   @app.route("/predict", methods = ["POST"])
    def predict():

    name = request.form.get("name")
    age = request.form.get("age")
    gender = request.form.get("gender")
    selected_symptoms = request.form.getlist("symptoms")

    input_data = [1 if symptom in selected_symptoms else 0 for symptoms in symptoms_list]
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
        name = name,
        disease = prediction,
        symptoms = selected_symptoms)