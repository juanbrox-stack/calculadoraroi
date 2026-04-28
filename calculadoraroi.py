import streamlit as st
import pandas as pd
import io

# 1. Configuración de la página ⚡
st.set_page_config(page_title="Calculadora de Productividad ⚡", layout="wide")

st.title("⚡ Calculadora de Ahorro de Tiempo")
st.write("Analiza cuántas horas recuperas al mes gracias a la automatización de procesos. ¡Optimiza tu flujo de trabajo! 🚀")

# 2. Sidebar: Parámetros generales (Comentados por si decides usarlos luego) ⚙️
st.sidebar.header("⚙️ Configuración")
# coste_hora = st.sidebar.number_input("Coste por hora empleado (€)", min_value=5.0, value=15.0, step=1.0)
# coste_app = st.sidebar.number_input("Coste automatización (€)", min_value=0.0, value=990.0, step=50.0)

# 3. Procesos (Datos iniciales con emojis) 📋
st.subheader("📋 Procesos a analizar")
procesos_base = [
    {"Proceso": "Dividir y limpiar Excel 🧹", "Tiempo manual (min)": 120, "Tiempo con app (min)": 10, "Frecuencia mensual": 12},
    {"Proceso": "Generar CSV para PrestaShop 🛒", "Tiempo manual (min)": 90, "Tiempo con app (min)": 5, "Frecuencia mensual": 8},
    {"Proceso": "Concatenar URLs y descargar 🔗", "Tiempo manual (min)": 60, "Tiempo con app (min)": 5, "Frecuencia mensual": 20},
    {"Proceso": "Preparar fichero marketplace 📦", "Tiempo manual (min)": 120, "Tiempo con app (min)": 15, "Frecuencia mensual": 10},
]

# Editor de datos dinámico
df_editado = st.data_editor(pd.DataFrame(procesos_base), num_rows="dynamic", use_container_width=True).fillna(0)

# 4. Lógica de Productividad (Cálculos de tiempo) ⏱️
df_editado["Horas ahorradas/mes"] = ((df_editado["Tiempo manual (min)"] - df_editado["Tiempo con app (min)"]) * df_editado["Frecuencia mensual"]) / 60

# --- CÁLCULOS MONETARIOS COMENTADOS ---
# df_editado["Ahorro mensual (€)"] = df_editado["Horas ahorradas/mes"] * coste_hora
# df_editado["Ahorro anual (€)"] = df_editado["Ahorro mensual (€)"] * 12

# Totales de tiempo
total_horas_mes = df_editado["Horas ahorradas/mes"].sum()
total_horas_anio = total_horas_mes * 12

# 5. Visualización de Resultados en Pantalla 📊
st.subheader("⏱️ Tiempo Recuperado Total")
c1, c2 = st.columns(2)
c1.metric("Horas ahorradas / mes 🗓️", f"{total_horas_mes:.1f} h")
c2.metric("Horas ahorradas / año 📅", f"{total_horas_anio:.1f} h")

# 6. Tabla de detalle para la Web
st.subheader("🔍 Detalle de productividad por proceso")
st.dataframe(
    df_editado.style.format({
        "Horas ahorradas/mes": "{:.2f}"
    }),
    use_container_width=True
)

# 7. Mensaje de Conclusión (Mensaje Comercial de Tiempo) 💡
st.subheader("💡 Conclusión del análisis")
st.success(
    f"""
    **¡Recupera tu jornada laboral!** 🌟
    
    Automatizando estos procesos, el equipo libera **{total_horas_mes:.1f} horas al mes**. 
    Esto equivale a recuperar aproximadamente **{total_horas_mes/8:.1f} días de trabajo** mensuales (jornadas de 8h) 
    que ahora pueden dedicarse a tareas de mayor valor creativo. ✨
    
    Al año, el ahorro total de tiempo es de **{total_horas_anio:.1f} horas** 🎯.
    """
)

# 8. Función para generar el Excel "PRO" (Formato Tabla y Colores) 🎨
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        sheet_name = 'Productividad'
        df.to_excel(writer, index=False, sheet_name=sheet_name)
        
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        
        # Dimensiones para la tabla
        (max_row, max_col) = df.shape
        column_settings = [{'header': column} for column in df.columns]
        
        # Añadir el formato "Tabla de Excel" (Estilo Pro con filtros y bandas de color)
        worksheet.add_table(0, 0, max_row, max_col - 1, {
            'columns': column_settings,
            'style': 'Table Style Medium 2', # Azul profesional
            'name': 'InformeProductividad'
        })
        
        # Formato de números y alineación
        f_decimal = workbook.add_format({'num_format': '0.00', 'align': 'center'})
        
        # Ajustes estéticos de columnas
        worksheet.set_column(0, 0, 40) # Columna de Proceso más ancha
        worksheet.set_column(1, max_col - 2, 18) # Columnas de datos intermedios
        worksheet.set_column(max_col - 1, max_col - 1, 25, f_decimal) # Columna de resultado final
        
    return output.getvalue()

# 9. Botón de exportación final 📥
st.divider()
excel_file = to_excel(df_editado)
st.download_button(
    label="📥 Descargar Informe Profesional de Productividad (Excel)",
    data=excel_file,
    file_name='analisis_eficiencia_equipo.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)