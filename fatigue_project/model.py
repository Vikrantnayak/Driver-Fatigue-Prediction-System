import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

# -----------------------------
# Synthetic Data Generation
# -----------------------------
def generate_synthetic_data(num_samples=3000, seed=42):
    np.random.seed(seed)
    data = {
        'Sleep_Hours': np.random.uniform(3, 12, num_samples),
        'Driving_Hours': np.random.uniform(0, 16, num_samples),
        'Caffeine_Cups': np.random.uniform(0, 5, num_samples),
        'Rest_Breaks': np.random.uniform(0, 120, num_samples),
        'Age': np.random.randint(18, 70, num_samples),
        'Stress_Level': np.random.uniform(1, 10, num_samples),
        'Time_of_Day': np.random.choice(['Morning', 'Afternoon', 'Night'], num_samples)
    }
    return pd.DataFrame(data)

# -----------------------------
# Fatigue Scoring Formula
# -----------------------------
def weighted_fatigue_score(row):
    score = 0
    score += max(0, 8 - row['Sleep_Hours']) * 1.5
    score += max(0, row['Driving_Hours'] - 6) * 1.2
    score += 0 if row['Caffeine_Cups'] >= 2 else 1.0
    score += max(0, 20 - row['Rest_Breaks']) * 0.1
    score += (row['Stress_Level'] - 5) * 0.5 if row['Stress_Level'] > 5 else 0
    if row['Time_of_Day'] == 'Night':
        score += 1.0
    return score

# -----------------------------
# Model Training
# -----------------------------
def train_model():
    df = generate_synthetic_data()
    df['Fatigue_Score'] = df.apply(weighted_fatigue_score, axis=1)
    df['Driver_Status'] = df['Fatigue_Score'].apply(lambda x: 'Fatigued' if x >= 5 else 'Alert')

    le_time = LabelEncoder()
    df['Time_of_Day_enc'] = le_time.fit_transform(df['Time_of_Day'])

    X = df[['Sleep_Hours', 'Driving_Hours', 'Caffeine_Cups', 'Rest_Breaks', 
            'Age', 'Stress_Level', 'Time_of_Day_enc']]
    y = df['Driver_Status']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)
    model.fit(X_scaled, y)

    return model, scaler, le_time

# -----------------------------
# Prediction Function
# -----------------------------
def predict_status(model, scaler, le_time, input_data):
    X = pd.DataFrame([{
        'Sleep_Hours': input_data['Sleep_Hours'],
        'Driving_Hours': input_data['Driving_Hours'],
        'Caffeine_Cups': input_data['Caffeine_Cups'],
        'Rest_Breaks': input_data['Rest_Breaks'],
        'Age': input_data['Age'],
        'Stress_Level': input_data['Stress_Level'],
        'Time_of_Day_enc': le_time.transform([input_data['Time_of_Day']])[0]
    }])

    X_scaled = scaler.transform(X)
    pred = model.predict(X_scaled)[0]
    probs = model.predict_proba(X_scaled)[0]
    confidence = float(probs.max())
    score = float(weighted_fatigue_score(input_data))

    return pred, confidence, score
