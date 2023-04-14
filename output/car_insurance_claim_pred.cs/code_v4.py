import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, confusion_matrix
import xgboost as xgb

def preprocess_data(data):
    # Process 'max_torque' and 'max_power' columns by extracting float numbers
    data['max_torque'] = data['max_torque'].apply(extract_float)
    data['max_power'] = data['max_power'].apply(extract_float)

    # Convert Boolean columns to 1 and 0
    for column in boolean_columns:
        data[column] = data[column].map({'Yes': 1, 'No': 0})

    # Convert categorical variables to numeric using LabelEncoder
    for col in categorical_columns:
        data[col] = le.fit_transform(data[col])
    
    return data

# Read and preprocess the dataset
data = pd.read_csv("insurance/train_qWM28Yl.csv")
target = data["is_claim"]
data = data.drop(["policy_id", "is_claim"], axis=1)

# Preprocess the data
data = preprocess_data(data)

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=42)

# Train and evaluate the Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, class_weight="balanced", random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

# Train and evaluate the XGBoost model
xgb_model = xgb.XGBClassifier(scale_pos_weight=1/0.06, random_state=42)
xgb_model.fit(X_train, y_train)
y_pred_xgb = xgb_model.predict(X_test)

# Compare F1 scores and confusion matrices
f1_rf = f1_score(y_test, y_pred_rf)
f1_xgb = f1_score(y_test, y_pred_xgb)

cm_rf = confusion_matrix(y_test, y_pred_rf)
cm_xgb = confusion_matrix(y_test, y_pred_xgb)

print("Random Forest F1 score: {:.4f}".format(f1_rf))
print("XGBoost F1 score: {:.4f}".format(f1_xgb))

print("Random Forest confusion matrix:")
print(cm_rf)

print("XGBoost confusion matrix:")
print(cm_xgb)