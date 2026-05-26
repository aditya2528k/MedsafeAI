import pandas as pd
import numpy as np
import pickle
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

dataset_path = os.path.join("dataset","symptoms_dataset.csv")
data = pd.read_csv(dataset_path)

print("✅ Dataset Loaded Successfully")
print("Dataset Shape:", data.shape)

x = data.drop("disease", axis = 1)
y = data["disease"]

symptoms_list = x.columns.tolist()

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)

model = DecisionTreeClassifier()
model.fit(x_train, y_train)
print("✅ Model Training Completed")

y_pred = model.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print("📊 Model Accuracy:", round(accuracy * 100, 2), "%")

os.makedirs("model", exist_ok = True)

model_path = os.path.join("model", "disease_model.pkl")
pickle.dump(model, open(model_path, "wb"))

print("✅ Model Saved Successfully")

symptoms_path = os.path.join("model", "symptoms_list.pkl")
pickle.dump(symptoms_list, open(symptoms_path, "wb"))

print("✅ Symptoms List Saved Successfully")
print("\n🎉 Training Process Completed Successfully!")