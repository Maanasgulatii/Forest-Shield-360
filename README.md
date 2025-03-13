# Forest-Shield-360

## Project Overview
**Forest-Shield-360** is an advanced **forest threat detection, prediction, and alert system** designed to identify potential environmental threats and provide timely alerts. This project integrates **machine learning models, reinforcement learning, and an automated alert system** to enhance early warning mechanisms and improve conservation efforts.


## Features
1. **Identification of 12 most common forest threats.**
2. **Simulation-based dataset generation** (3700 rows covering 45 days).
3. **Machine learning-based threat prediction** with multiple models.
4. **Reinforcement learning agent** to enhance threat forecasts.
5. **Automated alert system** using **Twilio API**.

---
## Modules
### 1. Detection
- Identifies **12 most likely to occur threats**: Deforestation, Drought, Disease, Fire, Flood, Landslide, Lightning, Overgrazing, Poaching, Pollution, Storm, and Earthquake.
- Simulates these threats in **MATLAB** to generate synthetic data.
- Dataset includes **3700 records spanning 45 days**.
- Features collected include date, threat name, temperature, precipitation, wildlife affected, threat type, and severity.

### 2. Prediction
- Uses the dataset to train various **machine learning models**:
  - **Decision Tree Model**
  - **XGBoost Model**
  - **Prophet Time-Series Model**
  - **Ensemble Learning Model (Decision Tree + XGBoost)**
  - **Reinforcement Learning Agent**
- Predicts:
  - **Threat severity (1-10 scale).**
  - **Environmental impact (temperature, precipitation, wildlife effect).**
  - **Most likely threat category.**
- **Joblib Model Files:**
  - `decision_tree_model.joblib` - Trained Decision Tree Classifier
  - `xgboost_model.joblib` - XGBoost Classifier
  - `prophet_models.joblib` - Prophet models for temperature, precipitation, and severity
  - `ensemble_model.joblib` - Combined model using Voting Classifier
  - `encoders.joblib` - Stores all necessary encoders for data transformation

### 3. Alert System
- **Twilio-based alert system** (`twilio_alerts.py`) sends messages when threat severity crosses predefined thresholds.
- Alerts include details on threat name, and its severity, or wildlife affected or forest health index, or all three of them based on the defined thresholds.

```python
import os
from twilio.rest import Client

def send_threat_alert(prediction_result):
    """
    Send SMS alert if threat conditions meet critical thresholds:
    - Severity > 7
    - Wildlife impact is 'High' or 'Severe'
    - Forest health index < 60
    
    Args:
        prediction_result (dict): The result dictionary from predict_threats()
    
    Returns:
        str or None: The Twilio message SID if sent, None otherwise
    """
    # Extract relevant values from prediction result
    threat_name = prediction_result['Most Likely Threat']
    date_str = prediction_result['Date']
    severity = prediction_result['Predicted Severity (1-10)']
    wildlife_impact = prediction_result['Predicted Wildlife Impact']
    forest_health_index = prediction_result['Forest Health Index (0-100)']
    
    # Check if any threshold is met
    should_alert = (
        severity > 7 or 
        wildlife_impact in ['High', 'Severe'] or 
        forest_health_index < 60
    )
    
    if not should_alert:
        print("No alert thresholds met. Skipping SMS notification.")
        return None
    
    # Construct alert message
    alert_reasons = []
    if severity > 7:
        alert_reasons.append(f"severity is {severity}/10")
    if wildlife_impact in ['High', 'Severe']:
        alert_reasons.append(f"wildlife impact is {wildlife_impact}")
    if forest_health_index < 60:
        alert_reasons.append(f"forest health index is {forest_health_index}")
    
    alert_reason = " and ".join(alert_reasons)
    
    message = (
        f"ALERT: '{threat_name}' is most likely to pose a threat to the forest on {date_str}. "
        f"The {alert_reason}. Please take action accordingly."
    )
    
    # Twilio credentials
    account_sid = 'Your account_sid'
    auth_token = 'Your auth_token'
    messaging_service_sid = 'Your messaging SSID'
    to_number = 'Your phone number' 
    
    # Initialize Twilio client and send message
    try:
        client = Client(account_sid, auth_token)
        message_sent = client.messages.create(
            messaging_service_sid=messaging_service_sid,
            body=message,
            to=to_number
        )
        print(f"Alert SMS sent! SID: {message_sent.sid}")
        print(f"Status: {message_sent.status}")
        return message_sent.sid
    except Exception as e:
        print(f"Failed to send SMS alert: {e}")
        return None
```

## Remember: 
- Make an account on twilio and verify your phone number first.
- It should contain '+' and the country code.
- You can change and define the thresholds according to your requirements.

---
## Installation Guide
Follow these steps to set up **Forest-Shield-360** on your local system:

### 1. Clone the Repository:
```bash
git clone https://github.com/Maanasgulatii/Forest-Shield-360.git
cd Forest-Shield-360
```

### 2. Install Dependencies:
 Store the requirements in a requirements.txt file. Then:
```bash
pip install -r requirements.txt
```

### 3. Run Data Preprocessing:
```bash
python scripts/load_data.py
```

### 4. Train Machine Learning Models:
```bash
python scripts/decision_tree_model.py
python scripts/xgboost_model.py
python scripts/prophet_model.py
python scripts/ensemble_model.py
python scripts/reinforcement_learning.py
```

### 5. Run Threat Prediction System:
```bash
python scripts/threat_prediction.py
```

---
Apart from this, **The Reinforcement Learning (RL)** agent in Forest-Shield-360 continuously learns and improves its threat prediction accuracy over time. It leverages insights from the other models, refining its predictions by dynamically adjusting its Q-values based on past outcomes. The RL agent tracks actual vs. predicted threats in a CSV file, analyzing discrepancies and updating its reward system to enhance accuracy. With each prediction, it fine-tunes its decision-making, ensuring more reliable threat forecasts and mitigation strategies with ongoing learning and adaptation. 

---
## Contribution Guidelines
- Fork the repository and create a new branch.
- Commit your changes and submit a pull request.

---
## License
This project is licensed under the **MIT License**.

