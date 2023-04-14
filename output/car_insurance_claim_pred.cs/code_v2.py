import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

# Helper function to extract first float from a string
def extract_float(text):
    import re
    result = re.findall(r'\d+.\d+', text)
    if result:
        return float(result[0])
    return None

# Read and preprocess the dataset
data = pd.read_csv("insurance/train_qWM28Yl.csv")

# Convert categorical variables to numeric using LabelEncoder
categorical_columns = ['area_cluster', 'make', 'segment', 'model', 'fuel_type', 'engine_type', 
                       'rear_brakes_type', 'transmission_type', 'steering_type']
le = LabelEncoder()
for col in categorical_columns:
    data[col] = le.fit_transform(data[col])

# Process 'max_torque' and 'max_power' columns by extracting float numbers
data['max_torque'] = data['max_torque'].apply(extract_float)
data['max_power'] = data['max_power'].apply(extract_float)

# Set aside the target column
target = data["is_claim"]
data = data.drop(["policy_id", "is_claim"], axis=1)

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=42)

# Train and evaluate the Random Forest model
model = RandomForestClassifier(n_estimators=100, max_depth=10, class_weight="balanced", random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

f1 = f1_score(y_test, y_pred)
print("F1 score: {:.4f}".format(f1))