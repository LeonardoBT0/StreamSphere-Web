import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

categories = [
    "Entretenimiento", "Educacion", "Musica", "Videojuegos",
    "Deportes", "Noticias", "Tecnologia", "Cocina",
    "Viajes", "Vlogs", "Cine", "Ciencia"
]

weekdays = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

records = []

for video_id in range(1, 501):
    duration_seconds = random.randint(30, 7200)
    category = random.choice(categories)
    publish_hour = random.randint(0, 23)
    publish_weekday = random.randint(0, 6)
    title_length = random.randint(10, 120)
    description_length = random.randint(0, 5000)
    is_hd = random.choice([0, 1])
    creator_subscribers = random.randint(0, 10_000_000)
    creator_avg_views_30d = random.randint(0, 500_000)

    score = 0

    if duration_seconds < 60:
        score += 1
    elif duration_seconds > 1800:
        score -= 1

    if category in ("Musica", "Entretenimiento", "Videojuegos"):
        score += 1
    elif category in ("Noticias", "Educacion"):
        score += 0

    if 8 <= publish_hour <= 12 or 18 <= publish_hour <= 22:
        score += 1
    else:
        score -= 1

    if publish_weekday >= 5:
        score += 1

    if 30 <= title_length <= 70:
        score += 1
    elif title_length > 100:
        score -= 1

    if description_length > 200:
        score += 1

    if is_hd == 1:
        score += 1

    if creator_subscribers > 100_000:
        score += 1
    elif creator_subscribers > 1_000_000:
        score += 1

    if creator_avg_views_30d > 10_000:
        score += 1
    elif creator_avg_views_30d > 100_000:
        score += 1

    if score <= 1:
        rendimiento = "BAJO"
    elif score <= 4:
        rendimiento = "MEDIO"
    else:
        rendimiento = "ALTO"

    records.append({
        "video_id": video_id,
        "duration_seconds": duration_seconds,
        "category": category,
        "publish_hour": publish_hour,
        "publish_weekday": publish_weekday,
        "title_length": title_length,
        "description_length": description_length,
        "is_hd": is_hd,
        "creator_subscribers": creator_subscribers,
        "creator_avg_views_30d": creator_avg_views_30d,
        "rendimiento_esperado": rendimiento
    })

df = pd.DataFrame(records)
df.to_csv("data/streamsphere_videos_dataset.csv", index=False)
print(f"Dataset generado: {len(df)} registros en data/streamsphere_videos_dataset.csv")
print(f"Distribucion: {df['rendimiento_esperado'].value_counts().to_dict()}")