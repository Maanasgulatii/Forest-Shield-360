import numpy as np
import random
import joblib
from collections import defaultdict
import sys
import os
from datetime import datetime
import pandas as pd
sys.path.append('D:/vscode/Forest Threat Detection/scripts')  # Keep original path

# File to store Q-table and metrics
RL_MODEL_PATH = '../models/rl_agent_model.joblib'
RL_METRICS_PATH = '../metrics/rl_performance.csv'

class RLAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.prediction_history = []  # Track prediction history for metrics
        self.accuracy = 0.0  # Track accuracy metric
        self.total_predictions = 0
        self.correct_predictions = 0

    def get_state(self, threat_type, temperature, precipitation):
        """Encodes the state based on threat and environmental conditions."""
        # Discretize continuous values to prevent state space explosion
        temp_bucket = round(temperature / 5) * 5  # Round to nearest 5 degrees
        precip_bucket = round(precipitation / 10) * 10  # Round to nearest 10mm
        return (threat_type, temp_bucket, precip_bucket)

    def choose_severity(self, state, possible_severities, confidence=None):
        """Selects severity prediction based on Q-values or exploration with confidence weighting."""
        # Use confidence to adjust exploration rate if provided
        effective_exploration = self.exploration_rate
        if confidence is not None:
            # Lower confidence means more exploration
            effective_exploration = self.exploration_rate * (1 + (1 - confidence))
        
        if random.uniform(0, 1) < effective_exploration:
            return random.choice(possible_severities)
        else:
            q_values = self.q_table[state]
            if not q_values:  # If no Q-values yet
                return random.choice(possible_severities)
            return max(q_values, key=q_values.get)

    def choose_mitigation(self, threat_type):
        """Selects the most effective mitigation strategy for a given threat."""
        if threat_type in MITIGATION_STRATEGIES:
            # Get the Q-values for this threat type's mitigations
            mitigation_values = defaultdict(float)
            
            # Check if we have any learned values for the mitigations
            for strategy in MITIGATION_STRATEGIES[threat_type]:
                # Use threat_type as part of the state for mitigation strategies
                mitigation_state = (threat_type, strategy)
                mitigation_values[strategy] = self.q_table.get(mitigation_state, {}).get('effectiveness', 0.0)
            
            # If we have learned values, use them
            if any(mitigation_values.values()):
                return max(mitigation_values.items(), key=lambda x: x[1])[0]
            
            # Otherwise, random selection
            return random.choice(MITIGATION_STRATEGIES[threat_type])
        return "No mitigation available."

    def update_q_value(self, state, severity, reward, next_state):
        """Updates the Q-value for severity prediction."""
        future_best = max(self.q_table[next_state].values(), default=0.0)
        old_value = self.q_table[state][severity]
        new_value = old_value + self.learning_rate * (reward + self.discount_factor * future_best - old_value)
        self.q_table[state][severity] = new_value

    def update_mitigation_q_value(self, threat_type, mitigation, effectiveness):
        """Updates the Q-value for mitigation strategies."""
        mitigation_state = (threat_type, mitigation)
        old_value = self.q_table.get(mitigation_state, {}).get('effectiveness', 0.0)
        new_value = old_value + self.learning_rate * (effectiveness - old_value)
        
        # Ensure the nested dictionary exists
        if mitigation_state not in self.q_table:
            self.q_table[mitigation_state] = {}
        
        self.q_table[mitigation_state]['effectiveness'] = new_value

    def predict_with_feedback(self, threat_type, temperature, precipitation, actual_severity, confidence=None):
        """Runs prediction and improves accuracy dynamically with feedback."""
        state = self.get_state(threat_type, temperature, precipitation)
        possible_severities = ["Low", "Medium", "High", "Severe"]
        predicted_severity = self.choose_severity(state, possible_severities, confidence)

        # Keep track for metrics
        self.total_predictions += 1
        is_correct = predicted_severity == actual_severity
        if is_correct:
            self.correct_predictions += 1
        
        # Update accuracy metrics
        self.accuracy = (self.correct_predictions / self.total_predictions) * 100

        # Assign reward: +1 if correct, -1 if incorrect, weighted by confidence if available
        reward_multiplier = 1.0
        if confidence is not None:
            reward_multiplier = confidence
        
        reward = reward_multiplier * (1 if is_correct else -1)
        self.update_q_value(state, predicted_severity, reward, state)

        # Record this prediction for later analysis
        self.prediction_history.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'threat_type': threat_type,
            'temperature': temperature,
            'precipitation': precipitation,
            'predicted_severity': predicted_severity,
            'actual_severity': actual_severity,
            'reward': reward,
            'is_correct': is_correct,
            'current_accuracy': self.accuracy
        })

        # Get best mitigation for this threat
        mitigation = self.choose_mitigation(threat_type)

        return predicted_severity, mitigation, self.accuracy

    def save_model(self):
        """Saves the Q-table to disk."""
        # Convert defaultdict to regular dict for serialization
        q_table_dict = {str(k): dict(v) for k, v in self.q_table.items()}
        
        # Create model directory if it doesn't exist
        os.makedirs(os.path.dirname(RL_MODEL_PATH), exist_ok=True)
        
        # Save agent state
        joblib.dump({
            'q_table': q_table_dict,
            'learning_rate': self.learning_rate,
            'discount_factor': self.discount_factor,
            'exploration_rate': self.exploration_rate,
            'total_predictions': self.total_predictions,
            'correct_predictions': self.correct_predictions,
            'accuracy': self.accuracy
        }, RL_MODEL_PATH)
        
        # Save metrics if we have prediction history
        if self.prediction_history:
            # Create metrics directory if it doesn't exist
            os.makedirs(os.path.dirname(RL_METRICS_PATH), exist_ok=True)
            
            # Convert prediction history to DataFrame and save
            metrics_df = pd.DataFrame(self.prediction_history)
            
            # Append to existing file if it exists
            if os.path.exists(RL_METRICS_PATH):
                existing_df = pd.read_csv(RL_METRICS_PATH)
                metrics_df = pd.concat([existing_df, metrics_df])
            
            metrics_df.to_csv(RL_METRICS_PATH, index=False)
            
        return True
    
    def load_model(self):
        """Loads the Q-table from disk if available."""
        if os.path.exists(RL_MODEL_PATH):
            try:
                saved_data = joblib.load(RL_MODEL_PATH)
                
                # Restore Q-table (convert string keys back to tuples)
                q_table_dict = saved_data['q_table']
                for k, v in q_table_dict.items():
                    # Convert string representation of tuple back to actual tuple
                    # This is a simplification - would need more robust parsing for production
                    try:
                        key = eval(k)  # Safe in this controlled context
                        self.q_table[key] = defaultdict(float, v)
                    except:
                        # If parsing fails, just use the string key
                        self.q_table[k] = defaultdict(float, v)
                
                # Restore other parameters
                self.learning_rate = saved_data.get('learning_rate', self.learning_rate)
                self.discount_factor = saved_data.get('discount_factor', self.discount_factor)
                self.exploration_rate = saved_data.get('exploration_rate', self.exploration_rate)
                self.total_predictions = saved_data.get('total_predictions', 0)
                self.correct_predictions = saved_data.get('correct_predictions', 0)
                self.accuracy = saved_data.get('accuracy', 0.0)
                
                return True
            except Exception as e:
                print(f"Error loading RL model: {e}")
                return False
        return False
    
    def get_performance_metrics(self):
        """Returns the current performance metrics of the RL agent."""
        return {
            'accuracy': self.accuracy,
            'total_predictions': self.total_predictions,
            'learning_rate': self.learning_rate,
            'exploration_rate': self.exploration_rate
        }

    def evaluate_mitigation(self, threat_type, mitigation, effectiveness_score):
        """Allow feedback on mitigation effectiveness (0-10 scale)."""
        # Normalize score to 0-1 range
        normalized_score = effectiveness_score / 10.0
        self.update_mitigation_q_value(threat_type, mitigation, normalized_score)
        
        # Save after each evaluation to preserve feedback
        self.save_model()

# Mitigation strategies with all threats included
MITIGATION_STRATEGIES = {
    'Deforestation': [
        "Implement reforestation programs.",
        "Enforce stricter logging regulations.",
        "Engage local communities in conservation efforts.",
        "Promote sustainable land-use practices.",
        "Increase monitoring of forest areas."
    ],
    'Drought': [
        "Implement water conservation strategies.",
        "Monitor drought indices closely.",
        "Develop drought-resistant vegetation plans.",
        "Educate farmers on sustainable practices during droughts.",
        "Establish water-sharing agreements among communities."
    ],
    'Disease': [
        "Conduct regular health checks on forest ecosystems.",
        "Implement disease management strategies for affected species.",
        "Increase research on disease-resistant species.",
        "Engage communities in monitoring wildlife health.",
        "Educate the public on disease prevention measures."
    ],
    'Fire': [
        "Increase controlled burns to reduce fuel load.",
        "Ensure firebreaks are well-maintained.",
        "Alert local fire services and prepare for rapid response.",
        "Conduct regular fire drills for local communities.",
        "Implement community awareness programs about fire safety."
    ],
    'Flood': [
        "Check and reinforce flood defenses.",
        "Clear drainage systems to prevent water accumulation.",
        "Prepare evacuation plans for low-lying areas.",
        "Monitor river levels closely during heavy rains.",
        "Educate communities about flood preparedness."
    ],
    'Landslide': [
        "Conduct geological assessments of vulnerable areas.",
        "Implement erosion control measures.",
        "Establish early warning systems for landslides.",
        "Engage local communities in monitoring activities.",
        "Reinforce infrastructure in landslide-prone zones."
    ],
    'Lightning': [
        "Install lightning protection systems in vulnerable areas.",
        "Educate communities about lightning safety measures.",
        "Conduct regular maintenance of tall structures to prevent strikes."
    ],
    'Overgrazing': [
        "Implement rotational grazing practices.",
        "Engage local farmers in sustainable grazing education.",
        "Monitor pasture health regularly to prevent degradation."
    ],
    'Poaching': [
        "Increase patrols in vulnerable wildlife areas.",
        "Engage community watch programs to report illegal activities.",
        "Collaborate with NGOs for wildlife protection initiatives."
    ],
    'Pollution': [
        "Implement stricter regulations on industrial waste disposal.",
        "Engage communities in clean-up efforts of polluted areas.",
        "Monitor air and water quality regularly."
    ],
    'Storm': [
        "Develop emergency response plans for severe weather events.",
        "Ensure infrastructure is resilient to storm impacts.",
        "Educate communities about storm preparedness and safety."
    ],
    'Earthquake': [
        "Reinforce critical infrastructure to withstand tremors.",
        "Develop and practice evacuation plans for high-risk areas.",
        "Monitor seismic activity and issue early warnings.",
        "Educate communities on earthquake safety measures."
    ]
}

# Create a global instance of the RL agent to maintain state between calls
_rl_agent = RLAgent()
# Try to load existing model
_rl_agent.load_model()

def reinforce_predictions(threat_type, severity_value, temperature=None, precipitation=None, confidence=None):
    """
    Enhanced function to be imported by threat_prediction.py that returns mitigation strategies
    based on the threat type, predicted severity, and environmental conditions.
    
    Args:
        threat_type (str): The type of threat predicted
        severity_value (int): The severity value (1-10)
        temperature (float, optional): The predicted temperature
        precipitation (float, optional): The predicted precipitation
        confidence (float, optional): The confidence score (0-1) of the prediction
    
    Returns:
        str: A recommended mitigation strategy
    """
    global _rl_agent
    
    # Map numeric severity to categorical
    severity_map = {
        1: "Low",
        2: "Low",
        3: "Low",
        4: "Medium",
        5: "Medium",
        6: "Medium",
        7: "High",
        8: "High",
        9: "Severe",
        10: "Severe"
    }
    
    # Get the categorical severity value (or default to "Medium" if not found)
    actual_severity = severity_map.get(severity_value, "Medium")
    
    # Use provided values if available, otherwise use defaults
    temp = temperature if temperature is not None else 25.0
    precip = precipitation if precipitation is not None else 10.0
    
    # Use the global RL agent to get a mitigation strategy
    _, mitigation, _ = _rl_agent.predict_with_feedback(threat_type, temp, precip, actual_severity, confidence)
    
    # Save the model to preserve learning
    _rl_agent.save_model()
    
    return mitigation

# For testing and analysis
def analyze_rl_performance():
    """
    Analyzes and displays the performance of the RL agent over time.
    
    Returns:
        dict: Performance metrics
    """
    global _rl_agent
    
    # Load metrics file if it exists
    if os.path.exists(RL_METRICS_PATH):
        metrics_df = pd.read_csv(RL_METRICS_PATH)
        
        # Get performance stats
        total_predictions = len(metrics_df)
        correct_predictions = metrics_df['is_correct'].sum()
        overall_accuracy = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0
        
        # Group by threat type to see performance by category
        threat_performance = metrics_df.groupby('threat_type').agg({
            'is_correct': ['mean', 'count']
        })
        
        # Calculate rolling accuracy
        if len(metrics_df) >= 10:
            metrics_df['rolling_accuracy'] = metrics_df['is_correct'].rolling(window=10).mean() * 100
        
        # Get current metrics from the agent
        agent_metrics = _rl_agent.get_performance_metrics()
        
        performance_data = {
            'overall_accuracy': overall_accuracy,
            'total_predictions': total_predictions,
            'agent_metrics': agent_metrics,
            'threat_performance': threat_performance.to_dict(),
            'accuracy_trend': metrics_df['current_accuracy'].tolist() if 'current_accuracy' in metrics_df.columns else []
        }
        
        return performance_data
    
    # If no metrics file exists, return current agent metrics
    return {'agent_metrics': _rl_agent.get_performance_metrics()}

def evaluate_mitigation_feedback(threat_type, mitigation, effectiveness_score):
    """
    Allows users to provide feedback on the effectiveness of suggested mitigations.
    
    Args:
        threat_type (str): The type of threat
        mitigation (str): The mitigation strategy that was applied
        effectiveness_score (int): How effective the strategy was (0-10)
    
    Returns:
        bool: Success status
    """
    global _rl_agent
    _rl_agent.evaluate_mitigation(threat_type, mitigation, effectiveness_score)
    return True

# Example usage
if __name__ == "__main__":
    # This section runs when the RL script is executed directly
    print("Forest Threat RL Agent Analysis")
    print("===============================")
    
    performance = analyze_rl_performance()
    
    print(f"\nOverall RL Agent Performance:")
    print(f"Current Accuracy: {performance.get('agent_metrics', {}).get('accuracy', 0):.2f}%")
    print(f"Total Predictions: {performance.get('agent_metrics', {}).get('total_predictions', 0)}")
    print(f"Learning Rate: {performance.get('agent_metrics', {}).get('learning_rate', 0)}")
    print(f"Exploration Rate: {performance.get('agent_metrics', {}).get('exploration_rate', 0)}")
    
    # Provide option to evaluate a previous mitigation
    try:
        evaluate_option = input("\nWould you like to evaluate a previous mitigation strategy? (y/n): ")
        if evaluate_option.lower() == 'y':
            threat_type = input("Enter the threat type (e.g., Fire, Drought): ")
            
            # Show available mitigations for this threat
            if threat_type in MITIGATION_STRATEGIES:
                print(f"\nAvailable mitigation strategies for {threat_type}:")
                for i, strategy in enumerate(MITIGATION_STRATEGIES[threat_type], 1):
                    print(f"{i}. {strategy}")
                
                strategy_num = int(input("\nEnter the number of the strategy you applied: "))
                if 1 <= strategy_num <= len(MITIGATION_STRATEGIES[threat_type]):
                    strategy = MITIGATION_STRATEGIES[threat_type][strategy_num-1]
                    effectiveness = float(input("Rate the effectiveness (0-10): "))
                    
                    evaluate_mitigation_feedback(threat_type, strategy, effectiveness)
                    print("\nThank you for your feedback! The RL agent will use this to improve future recommendations.")
            else:
                print(f"No mitigation strategies available for {threat_type}")
    except Exception as e:
        print(f"Error processing evaluation: {e}")