import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora ROI Automatización", layout="wide")

st.title("Calculadora de ROI por Automatización")
st.write("Calcula cuánto dinero puede ahorrar una pyme automatizando procesos manuales.")

st.sidebar.header("Parámetros generales")

coste_hora = st.sidebar.number_input(
    "Coste por hora del empleado (€)",
    min_value=5.0,
    value=15.0,
    step=1.0
)

coste_app = st.sidebar.number_input(
    "Coste estimado de la automatización (€)",
    min_value=0.0,
    value=990.0,
    step=50.0
)

st.subheader("Procesos a analizar")

procesos_base = [
    {
        "Proceso": "Dividir y limpiar Excel",
        "Tiempo manual (min)": 120,
        "Tiempo con app (min)": 10,
        "Frecuencia mensual": 12
    },
    {
        "Proceso": "Generar CSV para PrestaShop",
        "Tiempo manual (min)": 90,
        "Tiempo con app (min)": 5,
        "Frecuencia mensual": 8
    },
    {
        "Proceso": "Concatenar URLs y descargar archivos",
        "Tiempo manual (min)": 60,
        "Tiempo con app (min)": 5,
        "Frecuencia mensual": 20
    },
    {
        "Proceso": "Preparar fichero marketplace",
        "Tiempo manual (min)": 120,
        "Tiempo con app (min)": 15,
        "Frecuencia mensual": 10
    },
]

df = pd.DataFrame(procesos_base)

df_editado = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True
)

df_editado["Tiempo ahorrado mensual (h)"] = (
    (df_editado["Tiempo manual (min)"] - df_editado["Tiempo con app (min)"])
    * df_editado["Frecuencia mensual"]
) / 60

df_editado["Ahorro mensual (€)"] = df_editado["Tiempo ahorrado mensual (h)"] * coste_hora
df_editado["Ahorro anual (€)"] = df_editado["Ahorro mensual (€)"] * 12

ahorro_mensual_total = df_editado["Ahorro mensual (€)"].sum()
ahorro_anual_total = df_editado["Ahorro anual (€)"].sum()

if ahorro_mensual_total > 0:
    meses_recuperacion = coste_app / ahorro_mensual_total
else:
    meses_recuperacion = 0

st.subheader("Resultados")

col1, col2, col3 = st.columns(3)

col1.metric("Ahorro mensual", f"{ahorro_mensual_total:,.2f} €")
col2.metric("Ahorro anual", f"{ahorro_anual_total:,.2f} €")
col3.metric("Recuperación inversión", f"{meses_recuperacion:.1f} meses")

st.subheader("Detalle por proceso")

st.dataframe(
    df_editado.style.format({
        "Tiempo ahorrado mensual (h)": "{:.2f}",
        "Ahorro mensual (€)": "{:.2f} €",
        "Ahorro anual (€)": "{:.2f} €"
    }),
    use_container_width=True
)

st.subheader("Mensaje comercial")

st.success(
    f"""
    Automatizando estos procesos, la empresa podría ahorrar aproximadamente 
    **{ahorro_mensual_total:,.2f} € al mes** y **{ahorro_anual_total:,.2f} € al año**.

    Con una inversión estimada de **{coste_app:,.2f} €**, el retorno se conseguiría en 
    aproximadamente **{meses_recuperacion:.1f} meses**.
    """
)