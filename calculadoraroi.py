import streamlit as st
import pandas as pd
import io

# 1. Configuración de la página
st.set_page_config(page_title="Calculadora de Productividad ⚡", layout="wide")

st.title("⚡ Calculadora de Ahorro de Tiempo")
st.write("Analiza cuántas horas recuperas al mes gracias a la automatización de procesos. ¡Optimiza tu flujo de trabajo! 🚀")

# 2. Sidebar: Parámetros generales
st.sidebar.header("⚙️ Configuración")
# COMENTADO: Costes monetarios
# coste_hora = st.sidebar.number_input("Coste por hora empleado (€)", min_value=5.0, value=15.0, step=1.0)
# coste_app = st.sidebar.number_input("Coste automatización (€)", min_value=0.0, value=990.0, step=50.0)

# 3. Procesos (Datos iniciales)
st.subheader("📋 Procesos a analizar")
procesos_base = [
    {"Proceso": "Dividir y limpiar Excel 🧹", "Tiempo manual (min)": 120, "Tiempo con app (min)": 10, "Frecuencia mensual": 12},
    {"Proceso": "Generar CSV para PrestaShop 🛒", "Tiempo manual (min)": 90, "Tiempo con app (min)": 5, "Frecuencia mensual": 8},
    {"Proceso": "Concatenar URLs y descargar 🔗", "Tiempo manual (min)": 60, "Tiempo con app (min)": 5, "Frecuencia mensual": 20},
    {"Proceso": "Preparar fichero marketplace 📦", "Tiempo manual (min)": 120, "Tiempo con app (min)": 15, "Frecuencia mensual": 10},
]

# Editor de datos dinámico
df_editado = st.data_editor(pd.DataFrame(procesos_base), num_rows="dynamic", use_container_width=True).fillna(0)

# 4. Lógica de Productividad (Cálculos de tiempo)
df_editado["Horas ahorradas/mes"] = ((df_editado["Tiempo manual (min)"] - df_editado["Tiempo con app (min)"]) * df_editado["Frecuencia mensual"]) / 60

# Totales de tiempo
total_horas_mes = df_editado["Horas ahorradas/mes"].sum()
total_horas_anio = total_horas_mes * 12

# 5. Visualización de Resultados
st.subheader("⏱️ Tiempo Recuperado")
c1, c2 = st.columns(2)
c1.metric("Horas ahorradas / mes 🗓️", f"{total_horas_mes:.1f} h")
c2.metric("Horas ahorradas / año 📅", f"{total_horas_anio:.1f} h")

# 6. Tabla de detalle
st.subheader("🔍 Detalle de productividad por proceso")
st.dataframe(
    df_editado.style.format({
        "Horas ahorradas/mes": "{:.2f}"
    }),
    use_container_width=True
)

# 7. MENSAJE COMERCIAL (Enfocado en tiempo)
st.subheader("💡 Conclusión del análisis")
st.success(
    f"""
    **¡Recupera tu jornada laboral!** 🌟
    
    Automatizando estos procesos, el equipo libera **{total_horas_mes:.1f} horas al mes**. 
    Esto equivale a recuperar aproximadamente **{total_horas_mes/8:.1f} días de trabajo** mensuales 
    que ahora pueden dedicarse a tareas de mayor valor. ✨
    
    Al año, el ahorro total de tiempo es de **{total_horas_anio:.1f} horas** 🎯.
    """
)

# 8. Función para el Excel
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Productividad')
        workbook = writer.book
        worksheet = writer.sheets['Productividad']
        f_decimal = workbook.add_format({'num_format': '0.00'})
        worksheet.set_column('E:E', 20, f_decimal)
    return output.getvalue()

# 9. Botón de exportación
st.divider()
excel_file = to_excel(df_editado)
st.download_button(
    label="📥 Descargar Informe de Productividad (Excel)",
    data=excel_file,
    file_name='analisis_productividad.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)