import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Cargar datos
df = pd.read_csv("datos_kpi_escolares.csv")

# Etiquetar riesgo (solo para entrenar el modelo)
df["riesgo_academico"] = ((df["promedio_general"] < 6.0) |
                          (df["asistencia_porcentaje"] < 75) |
                          (df["cumplimiento_tareas_porcentaje"] < 60)).astype(int)

# Variables predictoras y objetivo
X = df[["promedio_general", "asistencia_porcentaje", "cumplimiento_tareas_porcentaje"]]
y = df["riesgo_academico"]

# División de datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar modelo
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Guardar modelo
joblib.dump(modelo, "modelo_riesgo_academico.pkl")
print("✅ Modelo entrenado y guardado con éxito.")
