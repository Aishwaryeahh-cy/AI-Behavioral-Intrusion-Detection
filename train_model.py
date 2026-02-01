import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

# Load dataset
data_path = 'data/login_behavior.csv'
df = pd.read_csv(data_path)

# Select features
features = ['typing_speed_ms', 'device_change', 'login_hour', 'location_change']
X = df[features]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train an Isolation Forest model
# contamination='auto' or 0.1 depending on expected anomaly rate. 
# Prompt doesn't specify parameter, but IsolationForest is requested.
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X_scaled)

# Save trained model and scaler
joblib.dump(model, 'login_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("Model training successful. Model and scaler saved.")
