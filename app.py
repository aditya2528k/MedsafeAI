from flask import Flask, render_template, request
import sqlite3
import pickle
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)

# -----------------------------
# Load Model
# -----------------------------
model_path = os.path.join("model", "disease_model.pkl")
symptoms_path = os.path.join("model", "symptoms_list.pkl")

model = pickle.load(open(model_path, "rb"))
symptoms_list = pickle.load(open(symptoms_path, "rb"))

# -----------------------------
# Database
# -----------------------------
DATABASE = os.path.join("instance", "medsafe.db")

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            symptoms TEXT,
            predicted_disease TEXT,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()

# Call once
init_db()

# -----------------------------
# Routes
# -----------------------------

@app.route("/")
def index():
    return render_template("index.html", symptoms=symptoms_list)

@app.route("/predict", methods=["POST"])
def predict():

    name = request.form.get("name")
    age = request.form.get("age")
    gender = request.form.get("gender")
    selected_symptoms = request.form.getlist("symptoms")

    input_data = [1 if symptom in selected_symptoms else 0 for symptom in symptoms_list]
    input_array = np.array([input_data])

    prediction = model.predict(input_array)[0]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO history (name, age, gender, symptoms, predicted_disease, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        age,
        gender,
        ", ".join(selected_symptoms),
        prediction,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return render_template("result.html",
                           name=name,
                           disease=prediction,
                           symptoms=selected_symptoms)

@app.route("/history")
def history():
    conn = get_db_connection()
    records = conn.execute("SELECT * FROM history ORDER BY date DESC").fetchall()
    conn.close()
    return render_template("history.html", records=records)

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)