import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.preprocessing import LabelEncoder
import joblib
import os

os.makedirs("models", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

df = pd.read_csv("data/streamsphere_videos_dataset.csv")
print(f"Dataset cargado: {len(df)} registros")

le_category = LabelEncoder()
df["category_encoded"] = le_category.fit_transform(df["category"])

feature_cols = [
    "duration_seconds", "category_encoded", "publish_hour",
    "publish_weekday", "title_length", "description_length",
    "is_hd", "creator_subscribers", "creator_avg_views_30d"
]

X = df[feature_cols]
y = df["rendimiento_esperado"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

clf = DecisionTreeClassifier(max_depth=3, random_state=42)
clf.fit(X_train, y_train)

joblib.dump(clf, "models/video_performance_tree.joblib")
joblib.dump(le_category, "models/label_encoder_category.joblib")
print("Modelo guardado en models/video_performance_tree.joblib")

y_pred = clf.predict(X_test)
accuracy = clf.score(X_test, y_test)
report = classification_report(y_test, y_pred)

with open("outputs/resultados_modelo.txt", "w") as f:
    f.write("=== REPORTE DEL MODELO DE ARBOL DE DECISION ===\n\n")
    f.write(f"Accuracy: {accuracy:.4f}\n\n")
    f.write("Reporte de clasificacion:\n")
    f.write(report)

print(f"Accuracy: {accuracy:.4f}")
print(f"Resultados guardados en outputs/resultados_modelo.txt")

plt.figure(figsize=(20, 12))
plot_tree(
    clf,
    feature_names=feature_cols,
    class_names=["BAJO", "MEDIO", "ALTO"],
    filled=True,
    rounded=True
)
plt.title("Arbol de Decision - Clasificacion de Rendimiento de Videos (max_depth=3)")
plt.savefig("outputs/arbol_decision.png", dpi=150, bbox_inches="tight")
plt.close()
print("Grafico del arbol guardado en outputs/arbol_decision.png")

cm = confusion_matrix(y_test, y_pred, labels=["BAJO", "MEDIO", "ALTO"])
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["BAJO", "MEDIO", "ALTO"]
)
fig, ax = plt.subplots(figsize=(8, 6))
disp.plot(ax=ax, cmap="Blues", values_format="d")
ax.set_title("Matriz de Confusion - Clasificacion de Rendimiento")
plt.savefig("outputs/matriz_confusion.png", dpi=150, bbox_inches="tight")
plt.close()
print("Matriz de confusion guardada en outputs/matriz_confusion.png")

print("Entrenamiento completado exitosamente.")