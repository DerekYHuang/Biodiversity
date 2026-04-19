import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. Load your merged data
df = pd.read_csv('dashboard_ecological_impact.csv')

# 2. Create a proxy "Clean Water" target (1 = Clean, 0 = Degraded)
# For this example: Clean water is above-median oxygen AND below-median nitrate
med_o2 = df['oxygen_umol_kg_mean'].median()
med_no3 = df['nitrate_umol_l_mean'].median()
df['clean_water'] = ((df['oxygen_umol_kg_mean'] > med_o2) & (df['nitrate_umol_l_mean'] < med_no3)).astype(int)

# 3. Train the Model
features = ['temperature_c_mean', 'nitrate_umol_l_mean']
# Fill missing values with means to prevent fitting errors
X = df[features].fillna(df[features].mean())
y = df['clean_water']

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)

# 4. Save Model for the Dashboard
joblib.dump(rf, 'clean_water_model.pkl')
print("Model saved to clean_water_model.pkl")