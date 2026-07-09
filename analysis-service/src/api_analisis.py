from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np

app = FastAPI(
    title="StreamSphere - Analysis Service",
    description="Microservicio de analisis de rendimiento de videos con Arbol de Decision",
    version="1.0.0"
)

clf = joblib.load("models/video_performance_tree.joblib")
le_category = joblib.load("models/label_encoder_category.joblib")

class VideoData(BaseModel):
    duration_seconds: int = Field(..., ge=1, le=7200)
    category: str = Field(...)
    publish_hour: int = Field(..., ge=0, le=23)
    publish_weekday: int = Field(..., ge=0, le=6)
    title_length: int = Field(..., ge=1, le=200)
    description_length: int = Field(..., ge=0, le=10000)
    is_hd: int = Field(..., ge=0, le=1)
    creator_subscribers: int = Field(..., ge=0)
    creator_avg_views_30d: int = Field(..., ge=0)

@app.get("/")
def root():
    return {
        "servicio": "StreamSphere Analysis Service",
        "version": "1.0.0",
        "estado": "operativo",
        "endpoints": {
            "/": "informacion del servicio",
            "/health": "estado del servicio",
            "/predict": "predecir rendimiento de un video (POST)"
        }
    }

@app.get("/health")
def health():
    modelo_cargado = clf is not None
    return {
        "status": "healthy" if modelo_cargado else "unhealthy",
        "modelo_cargado": modelo_cargado,
        "clases_disponibles": ["BAJO", "MEDIO", "ALTO"]
    }

@app.post("/predict")
def predict(data: VideoData):
    try:
        category_encoded = le_category.transform([data.category])[0]
    except ValueError:
        return {"error": f"Categoria '{data.category}' no reconocida. Categorias validas: {list(le_category.classes_)}"}

    input_df = pd.DataFrame([{
        "duration_seconds": data.duration_seconds,
        "category_encoded": category_encoded,
        "publish_hour": data.publish_hour,
        "publish_weekday": data.publish_weekday,
        "title_length": data.title_length,
        "description_length": data.description_length,
        "is_hd": data.is_hd,
        "creator_subscribers": data.creator_subscribers,
        "creator_avg_views_30d": data.creator_avg_views_30d
    }])

    pred = clf.predict(input_df)[0]
    probas = clf.predict_proba(input_df)[0]
    probabilidades = {
        cls: round(float(prob), 4)
        for cls, prob in zip(clf.classes_, probas)
    }

    recomendaciones = {
        "BAJO": "El video tiene baja probabilidad de buen rendimiento. Revisa la duracion, horario de publicacion y asegurate de que el titulo sea atractivo (30-70 caracteres).",
        "MEDIO": "El video tiene rendimiento moderado. Considera optimizar la descripcion (>200 caracteres) y publicar en horario de alta audiencia (8-12h o 18-22h).",
        "ALTO": "El video tiene alto potencial de rendimiento. Manten la calidad del contenido y la consistencia en las publicaciones."
    }

    return {
        "rendimiento_esperado": pred,
        "probabilidades": probabilidades,
        "recomendacion": recomendaciones[pred]
    }