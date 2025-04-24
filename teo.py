import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar archivo
df = pd.read_csv("Base_Simulada_con_50_Personas.csv")

# Título
st.title("Generador de Tablas Cruzadas Interactivas")

# Variables categóricas disponibles
# También incluir columnas numéricas con pocos valores únicos
categorical_columns = [col for col in df.columns if df[col].nunique() <= 10 or df[col].dtype == 'object']


# Selección de variables
var1 = st.selectbox("Variable para las filas (ej. Edad):", categorical_columns)
var2 = st.selectbox("Variable para las columnas (ej. Sexo):", categorical_columns)

if var1 != var2:
    # Tabla de frecuencias
    crosstab = pd.crosstab(df[var1], df[var2])
    crosstab["Total"] = crosstab.sum(axis=1)
    crosstab.loc["Total"] = crosstab.sum()
    st.subheader("🔢 Frecuencias Absolutas")
    st.dataframe(crosstab.astype(str))


    # Tabla de porcentajes
    percent = pd.crosstab(df[var1], df[var2], normalize='index') * 100
    percent = percent.round(2)
    st.subheader("📊 Porcentajes por Fila")
    st.dataframe(percent.astype(str))


    # Gráfico
    st.subheader("📈 Gráfico de Barras")
    fig, ax = plt.subplots()
    sns.countplot(data=df, x=var1, hue=var2, ax=ax)
    plt.title(f"Distribución de {var1} según {var2}")
    st.pyplot(fig)
else:
    st.warning("Selecciona dos variables distinaaaaatas.")
