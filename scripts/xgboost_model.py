import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
from load_data import load_data
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

def train_xgboost():
    df = load_data()

    # Encode 'Threat Type' using OneHotEncoder (same as other models)
    ohe_threat_type = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded_threat_type = ohe_threat_type.fit_transform(df[['Threat Type']])
    encoded_threat_type_df = pd.DataFrame(encoded_threat_type, columns=ohe_threat_type.get_feature_names_out(['Threat Type']))
    df = pd.concat([df.drop('Threat Type', axis=1).reset_index(drop=True), encoded_threat_type_df], axis=1)

    # Encode 'Threat Name' using LabelEncoder (XGBoost requires numerical labels)
    le_threat_name = LabelEncoder()
    df['Threat Name'] = le_threat_name.fit_transform(df['Threat Name'])

    X = df.drop(['Threat Name', 'Date', 'Wildlife Affected'], axis=1)
    y = df['Threat Name']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    xgb = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    xgb.fit(X_train, y_train)

    y_pred = xgb.predict(X_test)

    print("XGBoost Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred, target_names=le_threat_name.classes_))

    # Save the XGBoost model and label encoder
    joblib.dump(xgb, '../models/xgboost_model.joblib')
    joblib.dump(le_threat_name, '../models/encoders.joblib')  # Update encoders in the same file

if __name__ == "__main__":
    train_xgboost()
