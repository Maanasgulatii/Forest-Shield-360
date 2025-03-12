import pandas as pd
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
from load_data import load_data
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

def train_ensemble():
    """
    Train and save an ensemble model that combines Decision Tree and XGBoost
    for threat prediction.
    """
    df = load_data()

    # One-hot encode 'Threat Type' to match other models
    ohe_threat_type = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded_threat_type = ohe_threat_type.fit_transform(df[['Threat Type']])
    encoded_threat_type_df = pd.DataFrame(encoded_threat_type, columns=ohe_threat_type.get_feature_names_out(['Threat Type']))
    df = pd.concat([df.drop('Threat Type', axis=1).reset_index(drop=True), encoded_threat_type_df], axis=1)

    # Prepare features and target
    X = df.drop(['Threat Name', 'Date', 'Wildlife Affected'], axis=1)
    y = df['Threat Name']

    # Label encode the target for XGBoost
    le_threat_name = LabelEncoder()
    y_encoded = le_threat_name.fit_transform(y)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    # Create base models
    dt = DecisionTreeClassifier(max_depth=10, min_samples_split=5, random_state=42)
    xgb = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)

    # Create and train ensemble model (soft voting)
    ensemble = VotingClassifier(
        estimators=[('dt', dt), ('xgb', xgb)],
        voting='soft'  # Use soft voting to get probabilities
    )
    
    ensemble.fit(X_train, y_train)

    # Evaluate ensemble model
    y_pred = ensemble.predict(X_test)
    print("Ensemble Model Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred, target_names=le_threat_name.classes_))

    # Save encoders for prediction use
    # Include wildlife encoder from wildlife model or create a placeholder if needed
    le_wildlife = LabelEncoder()
    le_wildlife.fit(['Very Low', 'Low', 'Medium', 'High', 'Severe'])  # Basic wildlife impact levels
    
    # Save ensemble model
    joblib.dump(ensemble, '../models/ensemble_model.joblib')
    
    # Save encoders in consistent order
    joblib.dump((ohe_threat_type, le_threat_name, le_wildlife), '../models/encoders.joblib')
    
    print("Ensemble model and encoders saved successfully.")

if __name__ == "__main__":
    train_ensemble()