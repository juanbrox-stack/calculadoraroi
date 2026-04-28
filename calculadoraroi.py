import streamlit as st
import pandas as pd
import io

# Configuración de la página
st.set_page_config(page_title="Calculadora ROI Automatización", layout="wide")

st.title("Calculadora de ROI por Automatización")
st.write("Calcula cuánto dinero puede ahorrar una pyme automatizando procesos manuales.")

# --- SIDEBAR ---
st.sidebar.header("Parámetros generales")
coste_hora = st.sidebar.number_input("Coste por hora empleado (€)", min_value=5.0, value=15.0, step=1.0)
coste_app = st.sidebar.number_input("Coste automatización (€)", min_value=0.0, value=990.0, step=50.0)

# --- DATOS ---
procesos_base = [
    {"Proceso": "Dividir y limpiar Excel", "Tiempo manual (min)": 120, "Tiempo con app (min)": 10, "Frecuencia mensual": 12},
    {"Proceso": "Generar CSV para PrestaShop", "Tiempo manual (min)": 90, "Tiempo con app (min)": 5, "Frecuencia mensual": 8},
    {"Proceso": "Concatenar URLs y descargar archivos", "Tiempo manual (min)": 60, "Tiempo con app (min)": 5, "Frecuencia mensual": 20},
    {"Proceso": "Preparar fichero marketplace", "Tiempo manual (min)": 120, "Tiempo con app (min)": 15, "Frecuencia mensual": 10},
]

df_editado = st.data_editor(pd.DataFrame(procesos_base), num_rows="dynamic", use_container_width=True).fillna(0)

# Cálculos
df_editado["Tiempo ahorrado mensual (h)"] = ((df_editado["Tiempo manual (min)"] - df_editado["Tiempo con app (min)"]) * df_editado["Frecuencia mensual"]) / 60
df_editado["Ahorro mensual (€)"] = df_editado["Tiempo ahorrado mensual (h)"] * coste_hora
df_editado["Ahorro anual (€)"] = df_editado["Ahorro mensual (€)"] * 12

ahorro_mensual_total = df_editado["Ahorro mensual (€)"].sum()
ahorro_anual_total = df_editado["Ahorro anual (€)"].sum()
meses_recuperacion = coste_app / ahorro_mensual_total if ahorro_mensual_total > 0 else 0

# --- MÉTRICAS ---
col1, col2, col3 = st.columns(3)
col1.metric("Ahorro mensual", f"{ahorro_mensual_total:,.2f} €")
col2.metric("Ahorro anual", f"{ahorro_anual_total:,.2f} €")
col3.metric("Recuperación", f"{meses_recuperacion:.1f} meses")

# --- FUNCIÓN PARA GENERAR EXCEL FORMATEADO ---
def to_excel(df):
    output = io.BytesIO()
    # Usamos xlsxwriter como motor para dar formato
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Resumen ROI')
        
        workbook  = writer.book
        worksheet = writer.sheets['Resumen ROI']

        # Definimos formatos
        format_money = workbook.add_format({'num_format': '#,##0.00 €'})
        format_decimal = workbook.add_format({'num_format': '0.00'})

        # Aplicar formatos a las columnas (Letras según posición en el Excel)
        # E: Tiempo ahorrado, F: Ahorro mensual, G: Ahorro anual
        worksheet.set_column('E:E', 15, format_decimal)
        worksheet.set_column('F:G', 18, format_money)
        
    return output.getvalue()

# --- BOTÓN DE DESCARGA ---
st.divider()
excel_data = to_excel(df_editado)

st.download_button(
    label="📥 Descargar Informe en Excel (.xlsx)",
    data=excel_data,
    file_name='informe_roi.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)