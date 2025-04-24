import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# Cargar base de datos y diccionario
df = pd.read_csv("Base_Simulada_con_50_Personas.csv")
diccionario = pd.read_csv("Diccionario_Final_Usuario.csv")

# Estandarizar nombres de columnas
df.columns = df.columns.str.strip().str.upper()

# Limpiar y preparar diccionario
diccionario = diccionario.dropna(how='all').ffill()
diccionario = diccionario.dropna(subset=['INDICADOR', 'CODIFICACION'], how='all')

# Crear mapeo de variables del DataFrame a nombres descriptivos
nombre_variables = {}
for indicador in diccionario['INDICADOR'].dropna().unique():
    palabras = indicador.split()
    clave = palabras[-1].upper()  # Última palabra del indicador (ej. CODOS)
    if clave in df.columns:
        nombre_variables[clave] = indicador.upper()

# Filtrar variables que existan en el DataFrame y estén en el diccionario
sintomas_codificados = [col for col in df.columns if col in nombre_variables]
demograficas = ["EDAD", "BIOMASA", "TIEMPO", "EJERCICIO"]

st.title("🧾 Análisis de Pausas Activas y Síntomas Musculoesqueléticos")

# Función chi-cuadrado
def chi_test(var1, var2):
    tabla = pd.crosstab(df[var1], df[var2])
    chi2, p, dof, _ = chi2_contingency(tabla)
    return tabla, chi2, p

# Menú de análisis
analisis = st.selectbox("Selecciona el análisis que deseas realizar", [
    "1️⃣ Asociación entre IMC y síntomas musculoesqueléticos",
    "2️⃣ Asociación entre edad y síntomas musculoesqueléticos",
    "3️⃣ Comparación síntomas antes y después del programa",
    "4️⃣ Asociación entre ejercicios realizados y síntomas",
    "5️⃣ Caracterización sociodemográfica",
    "🔄 Análisis cruzado personalizado"
])

# Análisis según el caso
if analisis == "1️⃣ Asociación entre IMC y síntomas musculoesqueléticos":
    for var in sintomas_codificados:
        st.subheader(f"BIOMASA (IMC) vs {nombre_variables[var]}")
        tabla, chi2, p = chi_test("BIOMASA", var)
        st.write(tabla)
        st.download_button(
            label=f"📥 Descargar CSV - BIOMASA vs {nombre_variables[var]}",
            data=tabla.to_csv().encode('utf-8'),
            file_name=f"IMC_vs_{var}.csv",
            mime="text/csv"
        )
        st.write(f"Chi² = {chi2:.2f} | p-valor = {p:.4f}")
        st.success("✅ Asociación significativa" if p < 0.05 else "❌ No significativa")
elif analisis == "2️⃣ Asociación entre edad y síntomas musculoesqueléticos":
    for var in sintomas_codificados:
        st.subheader(f"EDAD vs {nombre_variables[var]}")
        tabla, chi2, p = chi_test("EDAD", var)
        st.write(tabla)
        st.download_button(
            label=f"📥 Descargar CSV - BIOMASA vs {nombre_variables[var]}",
            data=tabla.to_csv().encode('utf-8'),
            file_name=f"IMC_vs_{var}.csv",
            mime="text/csv"
        )
        st.write(f"Chi² = {chi2:.2f} | p-valor = {p:.4f}")
        st.success("✅ Asociación significativa" if p < 0.05 else "❌ No significativa")
elif analisis == "3️⃣ Comparación síntomas antes y después del programa":
    for var in sintomas_codificados:
        st.subheader(f"{nombre_variables[var]} - Antes vs Después")
        tabla, chi2, p = chi_test("TIEMPO", var)
        st.write(tabla)
        st.download_button(
            label=f"📥 Descargar CSV - BIOMASA vs {nombre_variables[var]}",
            data=tabla.to_csv().encode('utf-8'),
            file_name=f"IMC_vs_{var}.csv",
            mime="text/csv"
        )
        st.write(f"Chi² = {chi2:.2f} | p-valor = {p:.4f}")
        st.success("✅ Asociación significativa" if p < 0.05 else "❌ No significativa")

elif analisis == "4️⃣ Asociación entre ejercicios realizados y síntomas":
    if "EJERCICIO" in df.columns:
        for var in sintomas_codificados:
            st.subheader(f"EJERCICIO vs {nombre_variables[var]}")
            tabla, chi2, p = chi_test("EJERCICIO", var)
            st.write(tabla)
            st.download_button(
                label=f"📥 Descargar CSV - BIOMASA vs {nombre_variables[var]}",
                data=tabla.to_csv().encode('utf-8'),
                file_name=f"IMC_vs_{var}.csv",
                mime="text/csv"
            )
            st.write(f"Chi² = {chi2:.2f} | p-valor = {p:.4f}")
            st.success("✅ Asociación significativa" if p < 0.05 else "❌ No significativa")
    else:
        st.warning("⚠️ La variable EJERCICIO no está disponible en la base de datos.")

elif analisis == "5️⃣ Caracterización sociodemográfica":
    st.subheader("📊 Edad")
    st.write(df["EDAD"].describe())

    st.subheader("📊 IMC (BIOMASA)")
    st.write(df["BIOMASA"].value_counts(normalize=True) * 100)

    if "SEXO" in df.columns:
        st.subheader("📊 Sexo")
        st.write(df["SEXO"].value_counts(normalize=True) * 100)

elif analisis == "🔄 Análisis cruzado personalizado":
    columnas = [col for col in df.columns if df[col].nunique() <= 10 or df[col].dtype == 'object']
    var1 = st.selectbox("Variable para las filas:", columnas, key="fila")
    var2 = st.selectbox("Variable para las columnas:", columnas, key="columna")
    if var1 != var2:
        tabla, chi2, p = chi_test(var1, var2)
        st.subheader("📋 Tabla de contingencia")
        st.write(tabla)
        st.write(f"Chi² = {chi2:.2f} | p-valor = {p:.4f}")
        st.success("✅ Asociación significativa" if p < 0.05 else "❌ No significativa")
        st.download_button(
    label=f"📥 Descargar CSV - {var1} vs {var2}",
    data=tabla.to_csv().encode('utf-8'),
    file_name=f"{var1}_vs_{var2}.csv",
    mime="text/csv"
)
    else:
        st.warning("Selecciona variables distintas para el análisis.")
