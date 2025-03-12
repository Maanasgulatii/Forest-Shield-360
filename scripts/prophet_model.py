def predict_threat(threat_type, date_str):
    """
    Predict environmental conditions and severity for a specific threat type on a future date.
    
    Args:
        threat_type (str): The type of threat to predict for
        date_str (str): Date string in format "DD Month" or "DD Month YYYY"
    
    Returns:
        tuple: (predicted_severity, predicted_temp, predicted_precip, wildlife_impact)
    """
    import numpy as np
    import pandas as pd
    from datetime import datetime
    import joblib

    # Load models
    temp_model, precip_model, severity_model, wildlife_model = joblib.load('../models/prophet_models.joblib')
    ohe_threat_type, le_threat_name, le_wildlife = joblib.load('../models/encoders.joblib')

    # Handle date formatting
    if len(date_str.split()) == 2:
        current_year = datetime.now().year
        date_str += f" {current_year}"

    future_date = pd.to_datetime(date_str, format='%d %B %Y')

    # Prepare DataFrames for prediction
    future_temp_df = pd.DataFrame({'ds': [future_date]})
    future_precip_df = pd.DataFrame({'ds': [future_date]})
    future_severity_df = pd.DataFrame({'ds': [future_date]})

    # Predict values
    predicted_temp = temp_model.predict(future_temp_df)['yhat'].values[0]
    predicted_precip = precip_model.predict(future_precip_df)['yhat'].values[0]
    predicted_severity = round(severity_model.predict(future_severity_df)['yhat'].values[0])
    
    # Normalize the predicted severity to 1-10 range
    predicted_severity = max(1, min(10, abs(predicted_severity) % 10))
    if predicted_severity == 0:
        predicted_severity = 1

    # Map the threat type to encoded form
    threat_type_encoded = get_threat_type(threat_type)
    
    # One-hot encode the threat type
    threat_type_array = ohe_threat_type.transform([[threat_type_encoded]])
    
    # Wildlife impact prediction
    wildlife_input = np.hstack([[predicted_temp, predicted_precip, predicted_severity], threat_type_array])
    try:
        wildlife_encoded = wildlife_model.predict(wildlife_input)[0]
        wildlife_impact = le_wildlife.inverse_transform([wildlife_encoded])[0]
    except:
        # Fallback based on severity
        wildlife_mapping = {
            1: "Very Low", 2: "Very Low",
            3: "Low", 4: "Low",
            5: "Medium", 6: "Medium",
            7: "High", 8: "High",
            9: "Severe", 10: "Severe"
        }
        wildlife_impact = wildlife_mapping.get(predicted_severity, "Medium")

    return predicted_severity, predicted_temp, predicted_precip, wildlife_impact

def get_threat_type(threat_name):
    """Helper function to map threat names to their types"""
    threat_types = {
        'Deforestation': 'Human Made',
        'Drought': 'Natural',
        'Disease': 'Natural',
        'Fire': 'Natural',
        'Flood': 'Natural',
        'Landslide': 'Natural',
        'Lightning': 'Natural',
        'Overgrazing': 'Human Made',
        'Poaching': 'Human Made',
        'Pollution': 'Human Made',
        'Storm': 'Natural',
        'Earthquake': 'Natural'
    }
    return threat_types.get(threat_name, 'Unknown')