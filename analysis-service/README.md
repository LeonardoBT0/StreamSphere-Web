# StreamSphere - Analysis Service

Microservicio de analisis de rendimiento de videos para StreamSphere Web.
Clasifica el rendimiento esperado de un video en **BAJO**, **MEDIO** o **ALTO**
usando un Arbol de Decision entrenado con `scikit-learn`.

## Estructura del proyecto

```
analysis-service/
├── data/                           # Dataset CSV generado
│   └── streamsphere_videos_dataset.csv
├── models/                         # Modelo entrenado
│   ├── video_performance_tree.joblib
│   └── label_encoder_category.joblib
├── outputs/                        # Reportes y graficos
│   ├── arbol_decision.png
│   ├── matriz_confusion.png
│   └── resultados_modelo.txt
├── src/
│   ├── generar_dataset.py          # Genera dataset sintetico
│   ├── entrenar_modelo.py          # Entrena y evalua el modelo
│   └── api_analisis.py             # API REST con FastAPI
├── requirements.txt                # Dependencias Python
└── README.md                       # Este archivo
```

## Requisitos

- Python 3.10+
- pip

## Instalacion y ejecucion (Arch Linux)

### 1. Clonar el repositorio y entrar al modulo

```bash
cd analysis-service
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Generar el dataset

```bash
python src/generar_dataset.py
```

### 5. Entrenar el modelo

```bash
python src/entrenar_modelo.py
```

Esto generara:
- `models/video_performance_tree.joblib`
- `models/label_encoder_category.joblib`
- `outputs/arbol_decision.png`
- `outputs/matriz_confusion.png`
- `outputs/resultados_modelo.txt`

### 6. Iniciar la API

```bash
uvicorn src.api_analisis:app --reload --host 0.0.0.0 --port 8095
```

La API estara disponible en: http://localhost:8095

## Endpoints

### GET /
Informacion basica del servicio.

### GET /health
Estado del servicio y confirmacion de modelo cargado.

### POST /predict
Predice el rendimiento esperado de un video.

**Ejemplo de request:**

```json
{
  "duration_seconds": 420,
  "category": "Musica",
  "publish_hour": 20,
  "publish_weekday": 5,
  "title_length": 55,
  "description_length": 300,
  "is_hd": 1,
  "creator_subscribers": 500000,
  "creator_avg_views_30d": 25000
}
```

**Ejemplo de response:**

```json
{
  "rendimiento_esperado": "ALTO",
  "probabilidades": {
    "BAJO": 0.0,
    "MEDIO": 0.15,
    "ALTO": 0.85
  },
  "recomendacion": "El video tiene alto potencial de rendimiento. Manten la calidad del contenido y la consistencia en las publicaciones."
}
```

## Prueba rapida con curl

```bash
curl -X POST http://localhost:8095/predict \
  -H "Content-Type: application/json" \
  -d '{
    "duration_seconds": 300,
    "category": "Tecnologia",
    "publish_hour": 14,
    "publish_weekday": 3,
    "title_length": 50,
    "description_length": 250,
    "is_hd": 1,
    "creator_subscribers": 200000,
    "creator_avg_views_30d": 15000
  }'
```

## Variables del modelo

| Variable                  | Tipo   | Descripcion                          |
|---------------------------|--------|--------------------------------------|
| duration_seconds          | int    | Duracion del video en segundos        |
| category                  | string | Categoria del video                   |
| publish_hour              | int    | Hora de publicacion (0-23)            |
| publish_weekday           | int    | Dia de la semana (0=Lunes, 6=Domingo) |
| title_length              | int    | Longitud del titulo en caracteres     |
| description_length        | int    | Longitud de la descripcion            |
| is_hd                     | int    | 1 si es HD, 0 si no                   |
| creator_subscribers       | int    | Suscriptores del creador              |
| creator_avg_views_30d     | int    | Vistas promedio del creador (30 dias) |