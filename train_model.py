import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
import joblib

# Load German Credit Dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data"
column_names = ['checking_status','duration','credit_history','purpose','credit_amount','savings','employment','installment_rate','personal_status','other_debtors','residence_since','property','age','other_installment_plans','housing','existing_credits','job','num_dependents','telephone','foreign_worker','class']
df = pd.read_csv(url, sep=' ', names=column_names)

# Encode target
df['class'] = df['class'].map({1: 1, 2: 0})  # 1=good, 2=bad

# One-hot encode categorical variables
X = pd.get_dummies(df.drop('class', axis=1))
y = df['class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train XGBoost
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "xgb_model.pkl")
print("Model trained and saved.")
