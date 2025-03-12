# Forest-Shield-360

## Project Overview
**Forest-Shield-360** is an advanced **forest threat detection, prediction, and alert system** designed to identify potential environmental threats and provide timely alerts. This project integrates **machine learning models, reinforcement learning, and an automated alert system** to enhance early warning mechanisms and improve conservation efforts.

The system performs three key tasks:
- **Detection:** Identifies and categorizes 12 common forest threats using MATLAB-based simulations.
- **Prediction:** Forecasts future threats using **Decision Trees, XGBoost, Prophet models, Ensemble Learning, and Reinforcement Learning**.
- **Alert System:** Uses **Twilio API** to send alerts when predefined thresholds are exceeded.

## Features
1. **Identification of 12 common forest threats.**
2. **Simulation-based dataset generation** (3700 rows covering 45 days).
3. **Machine learning-based threat prediction** with multiple models.
4. **Reinforcement learning agent** to enhance threat forecasts.
5. **Automated alert system** using **Twilio API**.
6. **Forest Health Index calculation** for monitoring overall environmental conditions.

---
## Modules
### 1. Detection
- Identifies **12 common threats**: Deforestation, Drought, Disease, Fire, Flood, Landslide, Lightning, Overgrazing, Poaching, Pollution, Storm, and Earthquake.
- Simulates these threats in **MATLAB** to generate synthetic data.
- Dataset includes **3700 records spanning 45 days**.
- Features collected include temperature, precipitation, threat type, and severity.

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
- Alerts include details on **threat type, severity, and recommended actions**.

```python
# twilio_alerts.py (Embed this in README for users to copy)
from twilio.rest import Client

def send_threat_alert(threat_info):
    account_sid = "your_twilio_account_sid"
    auth_token = "your_twilio_auth_token"
    client = Client(account_sid, auth_token)
    
    message_body = f"ALERT: {threat_info['Most Likely Threat']} detected!\n" \
                   f"Severity: {threat_info['Predicted Severity (1-10)']}\n" \
                   f"Recommended Action: {threat_info['Suggested Action']}"
    
    message = client.messages.create(
        body=message_body,
        from_="your_twilio_phone_number",
        to="recipient_phone_number"
    )
    print(f"Alert Sent: {message.sid}")
```

---
## Installation Guide
Follow these steps to set up **Forest-Shield-360** on your local system:

### 1. Clone the Repository:
```bash
git clone https://github.com/Maanasgulatii/Forest-Shield-360.git
cd Forest-Shield-360
```

### 2. Install Dependencies:
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
## Adding Images to README
To upload images in your **README.md**:
1. **Add the image to your GitHub repository** (e.g., inside a `docs/images/` folder).
2. **Use the following Markdown syntax:**
   ```markdown
   ![Description](docs/images/example.png)
   ```
3. **If using an external image:**
   ```markdown
   ![Description](https://example.com/image.png)
   ```

---
## Future Enhancements
1. **Expand dataset** to include real-time environmental data.
2. **Enhance reinforcement learning** to improve threat mitigation strategies.
3. **Integrate GIS mapping** for real-time threat visualization.
4. **Deploy as a web app** for interactive threat monitoring.

---
## Contribution Guidelines
- Fork the repository and create a new branch.
- Commit your changes and submit a pull request.
- Follow best practices for **code formatting and documentation**.

---
## License
This project is licensed under the **MIT License**.

*Drop a ⭐ if you found Forest-Shield-360 useful!* 🌲🔥🌍

