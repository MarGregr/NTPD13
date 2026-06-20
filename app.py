from fastapi import FastAPI, HTTPException
from sklearn.linear_model import LinearRegression
import numpy as np
import os

#Inicjalizacja aplikacji z opisem
app = FastAPI(
    title="API Modelu ML - Laboratorium 03",
    description="API do serwowania modelu regresji liniowej z dwiema cechami",
    version="1.0.0"
)

#Przykładowe dane dla modelu y = 2*x1 + 3*x2
X_train = np.array([[1, 1], [1, 2], [2, 1], [2, 2], [3, 3], [5, 1]])
y_train = np.array([5, 8, 7, 10, 15, 13])

#Inicjalizacja i trenowanie modelu
model = LinearRegression()
model.fit(X_train, y_train)

@app.get("/")
async def root():
    return {"message": "Witaj w API!"}


@app.get("/info")
async def info():
    #Zwracanie informacji o modelu (typ, liczba cech)
    return {
        "model_type": type(model).__name__,
        "n_features": model.n_features_in_,
        "coefficients": [round(float(c), 2) for c in model.coef_],
        "intercept": round(float(model.intercept_), 2),
        "description": "Model przewiduje wynik na podstawie dwóch cech wejściowych (x1, x2)."
    }

@app.get("/health")
async def health():
    #Zwracanie informacji czy serwer jest w trybie online
    return {"status": "ok"}

@app.post("/predict")
async def predict(data: dict):
    #Sprawdzenie obecności kluczy x1 i x2
    if "x1" not in data or "x2" not in data:
        raise HTTPException(
            status_code=400,
            detail={"error": "Brak wymaganej wartości", "fields_required": ["x1", "x2"]}
        )

    #Walidacja typów danych
    try:
        input_x1 = float(data["x1"])
        input_x2 = float(data["x2"])
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=400,
            detail={"error": "Nieprawidłowy typ danych", "message": "Wartości x1 i x2 muszą być liczbami"}
        )

    #Wykonanie predykcji
    prediction = model.predict([[input_x1, input_x2]])

    return {
        "status": "success",
        "input": {"x1": input_x1, "x2": input_x2},
        "prediction": round(float(prediction[0]), 2)
    }

@app.get("/status")
async def get_status():
    #Nazwa klucza
    db_name = os.getenv("APP_DB_NAME", "default_db")
    return {"status": "running", "connected_to_db": db_name}