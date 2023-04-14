import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Read the data
train_data = pd.read_csv("insurance/train_qWM28Yl.csv")

# Preprocess categorical data
le = LabelEncoder()
train_data["area_cluster"] = le.fit_transform(train_data["area_cluster"])
train_data["segment"] = le.fit_transform(train_data["segment"])
train_data["fuel_type"] = le.fit_transform(train_data["fuel_type"])
train_data["engine_type"] = le.fit_transform(train_data["engine_type"])
train_data["rear_brakes_type"] = le.fit_transform(train_data["rear_brakes_type"])
train_data["transmission_type"] = le.fit_transform(train_data["transmission_type"])
train_data["steering_type"] = le.fit_transform(train_data["steering_type"])

# Convert boolean features to numeric
bool_cols = [col for col in train_data.columns if train_data[col].dtype == "object"]
for col in bool_cols:
    train_data[col] = train_data[col].apply(lambda x: 1 if x == "Yes" else 0)

# Split the dataset into training and validation sets
X = train_data.drop(["policy_id", "is_claim"], axis=1)
y = train_data["is_claim"]
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Predict on the validation set
y_pred = model.predict(X_valid)

# Print evaluation metrics
print(classification_report(y_valid, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_valid, y_pred))
print("Accuracy:", accuracy_score(y_valid, y_pred))