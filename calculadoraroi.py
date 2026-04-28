import streamlit as st
import pandas as pd
import io

# 1. Configuración de la página
st.set_page_config(page_title="Calculadora ROI Automatización", layout="wide")

st.title("Calculadora de ROI por Automatización")
st.write("Calcula cuánto dinero puede ahorrar una pyme automatizando procesos manuales.")

# 2. Sidebar: Parámetros generales
st.sidebar.header("Parámetros generales")
coste_hora = st.sidebar.number_input("Coste por hora empleado (€)", min_value=5.0, value=15.0, step=1.0)
coste_app = st.sidebar.number_input("Coste automatización (€)", min_value=0.0, value=990.0, step=50.0)

# 3. Procesos (Datos iniciales)
st.subheader("Procesos a analizar")
procesos_base = [
    {"Proceso": "Dividir y limpiar Excel", "Tiempo manual (min)": 120, "Tiempo con app (min)": 10, "Frecuencia mensual": 12},
    {"Proceso": "Generar CSV para PrestaShop", "Tiempo manual (min)": 90, "Tiempo con app (min)": 5, "Frecuencia mensual": 8},
    {"Proceso": "Concatenar URLs y descargar archivos", "Tiempo manual (min)": 60, "Tiempo con app (min)": 5, "Frecuencia mensual": 20},
    {"Proceso": "Preparar fichero marketplace", "Tiempo manual (min)": 120, "Tiempo con app (min)": 15, "Frecuencia mensual": 10},
]

# Editor de datos (Aquí el usuario puede añadir o quitar procesos)
df_editado = st.data_editor(pd.DataFrame(procesos_base), num_rows="dynamic", use_container_width=True).fillna(0)

# 4. Lógica de Negocio (Cálculos)
df_editado["Tiempo ahorrado mensual (h)"] = ((df_editado["Tiempo manual (min)"] - df_editado["Tiempo con app (min)"]) * df_editado["Frecuencia mensual"]) / 60
df_editado["Ahorro mensual (€)"] = df_editado["Tiempo ahorrado mensual (h)"] * coste_hora
df_editado["Ahorro anual (€)"] = df_editado["Ahorro mensual (€)"] * 12

ahorro_mensual_total = df_editado["Ahorro mensual (€)"].sum()
ahorro_anual_total = df_editado["Ahorro anual (€)"].sum()
meses_recuperacion = coste_app / ahorro_mensual_total if ahorro_mensual_total > 0 else 0

# 5. Visualización de Resultados (Métricas)
st.subheader("Resultados Globales")
c1, c2, c3 = st.columns(3)
c1.metric("Ahorro mensual", f"{ahorro_mensual_total:,.2f} €")
c2.metric("Ahorro anual", f"{ahorro_anual_total:,.2f} €")
c3.metric("Recuperación", f"{meses_recuperacion:.1f} meses")

# 6. Tabla de detalle formateada para la web
st.subheader("Detalle por proceso")
st.dataframe(
    df_editado.style.format({
        "Tiempo ahorrado mensual (h)": "{:.2f}",
        "Ahorro mensual (€)": "{:.2f} €",
        "Ahorro anual (€)": "{:.2f} €"
    }),
    use_container_width=True
)

# 7. MENSAJE COMERCIAL (Asegurado que aparezca aquí)
st.subheader("Conclusión del análisis")
st.success(
    f"""
    **¡Gran oportunidad de optimización!**
    
    Automatizando estos procesos, tu empresa podría ahorrar **{ahorro_mensual_total:,.2f} € al mes** y un total de **{ahorro_anual_total:,.2f} € al año**.

    Considerando la inversión de **{coste_app:,.2f} €**, el retorno de inversión (ROI) 
    se alcanza en tan solo **{meses_recuperacion:.1f} meses**.
    """
)

# 8. Función para el Excel formateado
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Informe ROI')
        workbook = writer.book
        worksheet = writer.sheets['Informe ROI']
        # Formatos de moneda y números
        f_money = workbook.add_format({'num_format': '#,##0.00 €'})
        f_decimal = workbook.add_format({'num_format': '0.00'})
        worksheet.set_column('E:E', 15, f_decimal)
        worksheet.set_column('F:G', 18, f_money)
    return output.getvalue()

# 9. Botón de exportación
st.divider()
excel_file = to_excel(df_editado)
st.download_button(
    label="📥 Descargar Informe Profesional en Excel",
    data=excel_file,
    file_name='informe_roi_automatizacion.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)