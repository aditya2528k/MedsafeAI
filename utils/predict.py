import pickle
import numpy as np
import os

model_path = os.path.join("model", "disease_model.pkl")
symptoms_path = os.path.join("model", "symptoms_list.pkl")

model = pickle.load(open(model_path, "rb"))
symptoms_list = pickle.load(open(symptoms_path, "rb"))

def predict_disease(selected_symptoms):
    input_data = [1 if symptom in selected_symptoms else 0 for symptom in symptoms_list]
    input_array = np.array([input_data])
    prediction = model.predict(input_array)[0]
    return prediction

