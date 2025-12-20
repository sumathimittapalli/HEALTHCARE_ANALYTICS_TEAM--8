def preprocess_input(data):
    """
    Turn Pydantic object into the list of features expected by the model.
    Order: [age, gender_male, blood_pressure, sugar, bmi, cholesterol]
    We encode gender as 1 for male, 0 for female (simple encoding).
    """
    gender_male = 1 if data.gender.lower() in ("male", "m") else 0
    return [
        data.age,
        gender_male,
        data.blood_pressure,
        data.sugar,
        data.bmi,
        data.cholesterol
    ]
