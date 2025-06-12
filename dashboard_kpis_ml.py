import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# Config
st.set_page_config(page_title="Dashboard Escolar", layout="wide")

# Cargar modelo y datos
modelo = joblib.load("modelo_riesgo_academico.pkl")
df = pd.read_csv("datos_kpi_escolares.csv")

st.write("✅ Archivo CSV cargado con éxito")
st.write(df.head())

# Predecir riesgo usando el modelo
X_pred = df[["promedio_general", "asistencia_porcentaje", "cumplimiento_tareas_porcentaje"]]
df["riesgo_predicho"] = modelo.predict(X_pred)


# Obtener probabilidades del modelo
df["prob_riesgo"] = modelo.predict_proba(X_pred)[:, 1]

# Clasificar niveles de riesgo
def clasificar_nivel(prob):
    if prob >= 0.75:
        return "Alto"
    elif prob >= 0.5:
        return "Medio"
    else:
        return "Bajo"

df["nivel_riesgo"] = df["prob_riesgo"].apply(clasificar_nivel)


# Título
st.title("📊 Dashboard Escolar con IA - Riesgo Académico")

# Filtros opcionales
with st.sidebar:
    st.header("📌 Filtros")
    grado = st.selectbox("Selecciona grado", options=["Todos"] + sorted(df["grado"].unique()))
    periodo = st.selectbox("Selecciona periodo", options=["Todos"] + sorted(df["periodo_evaluacion"].unique()))
    if grado != "Todos":
        df = df[df["grado"] == grado]
    if periodo != "Todos":
        df = df[df["periodo_evaluacion"] == periodo]

# KPI: Riesgo académico predicho
st.subheader("🧠 Estudiantes en Riesgo (Modelo ML)")
riesgo_count = df["riesgo_predicho"].sum()
total = df.shape[0]
st.metric("En Riesgo", f"{riesgo_count}", f"de {total} estudiantes")

fig_riesgo = px.pie(df, names="riesgo_predicho", title="Riesgo Académico (Modelo ML)",
                    color_discrete_map={1: "red", 0: "green"},
                    labels={1: "En riesgo", 0: "No en riesgo"})
st.plotly_chart(fig_riesgo, use_container_width=True)

st.subheader("📋 Lista de estudiantes con nivel de riesgo")


# Seleccionar columnas para mostrar
tabla_riesgo = df[["nombre_estudiante", "grado", "periodo_evaluacion", "promedio_general", "asistencia_porcentaje",
                   "cumplimiento_tareas_porcentaje", "nivel_riesgo"]]

# Ordenar por nivel de riesgo (opcional)
orden_riesgo = {"Alto": 0, "Medio": 1, "Bajo": 2}
tabla_riesgo["orden"] = tabla_riesgo["nivel_riesgo"].map(orden_riesgo)
tabla_riesgo = tabla_riesgo.sort_values("orden")


# Mostrar tabla
st.dataframe(tabla_riesgo.drop("orden", axis=1), use_container_width=True)


# ----------------------------
# KPI 2: Promedio Académico General
# ----------------------------
st.subheader("📈 Promedio Académico General")

promedio_total = round(df["promedio_general"].mean(), 2)
st.metric("Promedio General", f"{promedio_total}/10")

fig_promedio = px.histogram(df, x="promedio_general", nbins=20, title="Distribución del Promedio General",
                            color_discrete_sequence=["#2ca02c"])
st.plotly_chart(fig_promedio, use_container_width=True)

# ----------------------------
# KPI 3: Asistencia Estudiantil
# ----------------------------
st.subheader("📅 Asistencia Estudiantil")

asistencia_media = round(df["asistencia_porcentaje"].mean(), 2)
st.metric("Asistencia Promedio", f"{asistencia_media}%")

fig_asistencia = px.box(df, y="asistencia_porcentaje", points="all",
                        title="Distribución de Asistencia por Estudiante",
                        color_discrete_sequence=["#1f77b4"])
st.plotly_chart(fig_asistencia, use_container_width=True)

# ----------------------------
# KPI 4: Cumplimiento de Tareas
# ----------------------------
st.subheader("✅ Cumplimiento de Tareas")

cumplimiento_medio = round(df["cumplimiento_tareas_porcentaje"].mean(), 2)
st.metric("Cumplimiento Promedio", f"{cumplimiento_medio}%")

fig_cumplimiento = px.box(df, y="cumplimiento_tareas_porcentaje", points="all",
                          title="Cumplimiento de Tareas por Estudiante",
                          color_discrete_sequence=["#ff7f0e"])
st.plotly_chart(fig_cumplimiento, use_container_width=True)