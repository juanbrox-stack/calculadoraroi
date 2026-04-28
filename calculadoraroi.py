import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Calculadora ROI Automatización", layout="wide")

st.title("Calculadora de ROI por Automatización")
st.write("Calcula cuánto dinero puede ahorrar una pyme automatizando procesos manuales.")

# --- SIDEBAR: ENTRADA DE COSTES GLOBALES ---
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

# --- CUERPO PRINCIPAL: EDITOR DE PROCESOS ---
st.subheader("Procesos a analizar")
st.info("Puedes editar los procesos existentes, añadir nuevos al final de la tabla o borrarlos.")

procesos_base = [
    {"Proceso": "Dividir y limpiar Excel", "Tiempo manual (min)": 120, "Tiempo con app (min)": 10, "Frecuencia mensual": 12},
    {"Proceso": "Generar CSV para PrestaShop", "Tiempo manual (min)": 90, "Tiempo con app (min)": 5, "Frecuencia mensual": 8},
    {"Proceso": "Concatenar URLs y descargar archivos", "Tiempo manual (min)": 60, "Tiempo con app (min)": 5, "Frecuencia mensual": 20},
    {"Proceso": "Preparar fichero marketplace", "Tiempo manual (min)": 120, "Tiempo con app (min)": 15, "Frecuencia mensual": 10},
]

# Creamos el editor de datos dinámico
df_editado = st.data_editor(
    pd.DataFrame(procesos_base),
    num_rows="dynamic",
    use_container_width=True
)

# Limpieza: Rellenamos valores vacíos con 0 para evitar errores en los cálculos
df_editado = df_editado.fillna(0)

# --- CÁLCULOS LOGICOS ---
# Calculamos el ahorro en horas y dinero
df_editado["Tiempo ahorrado mensual (h)"] = (
    (df_editado["Tiempo manual (min)"] - df_editado["Tiempo con app (min)"])
    * df_editado["Frecuencia mensual"]
) / 60

df_editado["Ahorro mensual (€)"] = df_editado["Tiempo ahorrado mensual (h)"] * coste_hora
df_editado["Ahorro anual (€)"] = df_editado["Ahorro mensual (€)"] * 12

# Totales globales
ahorro_mensual_total = df_editado["Ahorro mensual (€)"].sum()
ahorro_anual_total = df_editado["Ahorro anual (€)"].sum()

# Cálculo del Payback (Recuperación de la inversión)
if ahorro_mensual_total > 0:
    meses_recuperacion = coste_app / ahorro_mensual_total
else:
    meses_recuperacion = 0

# --- VISUALIZACIÓN DE RESULTADOS ---
st.subheader("Resultados Globales")
col1, col2, col3 = st.columns(3)

col1.metric("Ahorro mensual", f"{ahorro_mensual_total:,.2f} €")
col2.metric("Ahorro anual", f"{ahorro_anual_total:,.2f} €")
col3.metric("Retorno inversión", f"{meses_recuperacion:.1f} meses")

# Detalle técnico formateado
st.subheader("Detalle por proceso")
st.dataframe(
    df_editado.style.format({
        "Tiempo ahorrado mensual (h)": "{:.2f}",
        "Ahorro mensual (€)": "{:.2f} €",
        "Ahorro anual (€)": "{:.2f} €"
    }),
    use_container_width=True
)

# Mensaje comercial dinámico
st.subheader("Conclusión del informe")
st.success(
    f"""
    **Resumen ejecutivo:**
    
    Al automatizar estos procesos, la empresa deja de gastar **{ahorro_mensual_total:,.2f} € al mes** en tareas repetitivas. 
    Esto supone un ahorro total de **{ahorro_anual_total:,.2f} € al año**.

    Con una inversión inicial de **{coste_app:,.2f} €**, la herramienta se paga sola en **{meses_recuperacion:.1f} meses**. 
    A partir de ahí, todo es beneficio neto para la empresa.
    """
)

# --- BOTÓN DE DESCARGA ---
st.divider()
csv = df_editado.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Descargar Informe Completo (CSV)",
    data=csv,
    file_name='informe_roi_automatizacion.csv',
    mime='text/csv',
)