import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
from load_data import load_data
from sklearn.preprocessing import OneHotEncoder

def train_decision_tree():
    df = load_data()

    # One-hot encode 'Threat Type' to match prophet_model.py
    ohe_threat_type = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded_threat_type = ohe_threat_type.fit_transform(df[['Threat Type']])
    encoded_threat_type_df = pd.DataFrame(encoded_threat_type, columns=ohe_threat_type.get_feature_names_out(['Threat Type']))
    df = pd.concat([df.drop('Threat Type', axis=1).reset_index(drop=True), encoded_threat_type_df], axis=1)

    X = df.drop(['Threat Name', 'Date', 'Wildlife Affected'], axis=1)
    y = df['Threat Name']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    dt = DecisionTreeClassifier(max_depth=10, min_samples_split=5, random_state=42)
    dt.fit(X_train, y_train)

    y_pred = dt.predict(X_test)

    print("Decision Tree Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    # Save Decision Tree model
    joblib.dump(dt, '../models/decision_tree_model.joblib')

if __name__ == "__main__":
    train_decision_tree()
