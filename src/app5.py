import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------
# Conectar a la base de datos
# -------------------------------------------------------------------------
conexion = sqlite3.connect(r"C:\Users\jaid_\OneDrive\Escritorio\Proyecto_final\datos.db")
cursor = conexion.cursor()

# -------------------------------------------------------------------------
# Interfaz en Streamlit
# -------------------------------------------------------------------------
st.title("Pronóstico de Delitos en CDMX")
st.image(r"C:\Users\jaid_\OneDrive\Escritorio\Proyecto_final\Mexico_City_Reforma_Street.jpg",
         caption="Ciudad de México", use_container_width=True)

# -------------------------------------------------------------------------
# Consulta SQL
# -------------------------------------------------------------------------
cursor.execute('''
    SELECT
        P.fecha_hecho AS Fecha, COUNT(*) AS Recuento
    FROM tablaPrincipal P
    JOIN tablaAlcaldias A
        ON P.id_alcaldia_hecho = A.alcaldia_id
    JOIN tablaColonias C
        ON P.id_colonia_hecho = C.colonia_id
    WHERE
        P.categoria_delito = "DELITO DE BAJO IMPACTO"
        AND C.Colonia = "INFONAVIT IZTACALCO"
        AND A.Alcaldia = "IZTACALCO"
    GROUP BY P.fecha_hecho
    ORDER BY P.fecha_hecho
''')

resultados = cursor.fetchall()
columnas = [descripcion[0] for descripcion in cursor.description]
dfAgrupado = pd.DataFrame(resultados, columns=columnas)
dfAgrupado["Fecha"] = pd.to_datetime(dfAgrupado["Fecha"])

# -------------------------------------------------------------------------
# Manejo de fechas faltantes
# -------------------------------------------------------------------------
fechas = pd.date_range(start='2015-10-07', end='2024-09-26')
dfFechas = pd.DataFrame({"Fecha": fechas})
dfTotal = pd.merge(dfFechas, dfAgrupado, how="left", on=['Fecha'])
dfTotal['Recuento'] = dfTotal['Recuento'].fillna(0)

# -------------------------------------------------------------------------
# Visualización del historial de delitos
# -------------------------------------------------------------------------
st.subheader("Historial de delitos")
fig, ax = plt.subplots()
ax.plot(dfTotal["Fecha"], dfTotal["Recuento"], marker='', linestyle='-', color='r')
ax.set_title("Delitos")
ax.set_xlabel("Fecha")
ax.set_ylabel("Cantidad de delitos")
plt.xticks(rotation=45)
st.pyplot(fig)

# -------------------------------------------------------------------------
# Mostrar los mapas en paralelo
# -------------------------------------------------------------------------

st.markdown(
    "<h3 style='text-align: center;'>Mapas de incidencia delictiva</h3>", 
    unsafe_allow_html=True
)

# Definir columnas con mayor ancho
col1, col2, col3 = st.columns([5,5,5])  # Aumentar proporción para hacerlas más anchas

with col1:
    st.subheader("Mapa de incidencia")
    with open(r"C:\Users\jaid_\OneDrive\Escritorio\Proyecto_final\mapa_delitos.html", "r", encoding="utf-8") as f:
        mapa1_html = f.read()
    st.components.v1.html(mapa1_html, height=500)

with col2:
    st.subheader("Distribución geográfica")
    with open(r"C:\Users\jaid_\OneDrive\Escritorio\Proyecto_final\mapa_delitos_bajo_impacto.html", "r", encoding="utf-8") as f:
        mapa2_html = f.read()
    st.components.v1.html(mapa2_html, height=500)

with col3:
    st.subheader("Delitos comunes por alcaldía")
    with open(r"C:\Users\jaid_\OneDrive\Escritorio\Proyecto_final\mapa_delitos_comunes_alcaldia.html", "r", encoding="utf-8") as f:
        mapa3_html = f.read()
    st.components.v1.html(mapa3_html, height=500)

# -------------------------------------------------------------------------
# Cerrar la conexión
# -------------------------------------------------------------------------
conexion.close()