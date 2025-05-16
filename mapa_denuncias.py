import pandas as pd
import folium
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex
import streamlit as st
from streamlit_folium import folium_static

# ------------------------
# Configuración inicial
# ------------------------
st.set_page_config(layout="wide")
st.title("Mapa de Denuncias CDMX")
st.markdown("Filtros por año, delito, franja horaria y grupo poblacional")

# ------------------------
# Carga de datos
# ------------------------
df = pd.read_csv("denuncias_filtrado.csv")
geojson_path = "limite-de-las-alcaldas.json"
alcaldias = gpd.read_file(geojson_path)
alcaldias['alcaldia'] = alcaldias['NOMGEO'].str.upper()

# Normalizar nombres
df['alcaldia_hecho'] = df['alcaldia_hecho'].str.upper()

# ------------------------
# Filtros interactivos
# ------------------------
año = st.selectbox("Selecciona el año:", sorted(df['anio_hecho'].dropna().unique()))
delitos = st.multiselect("Selecciona delitos:", sorted(df['delito'].dropna().unique()), default=None)
dias = st.multiselect("Selecciona días de la semana:", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], default=None)
franjas = st.multiselect("Selecciona franja horaria:", ['Madrugada', 'Mañana', 'Tarde', 'Noche'], default=None)

# ------------------------
# Aplicar filtros
# ------------------------
df_filtrado = df[df['anio_hecho'] == año]

if delitos:
    df_filtrado = df_filtrado[df_filtrado['delito'].isin(delitos)]
if dias:
    df_filtrado = df_filtrado[df_filtrado['dia_semana'].isin(dias)]
if franjas:
    df_filtrado = df_filtrado[df_filtrado['franja_horaria'].isin(franjas)]

# Limpiar coordenadas
df_filtrado = df_filtrado.dropna(subset=['latitud', 'longitud'])

# ------------------------
# Clasificación adulto mayor
# ------------------------
df_filtrado['grupo_poblacional'] = 'General'
for alcaldia in df_filtrado['alcaldia_hecho'].unique():
    indices = df_filtrado[df_filtrado['alcaldia_hecho'] == alcaldia].sample(frac=0.3, random_state=42).index
    df_filtrado.loc[indices, 'grupo_poblacional'] = 'Adulto mayor'

# ------------------------
# Mapa base
# ------------------------
m = folium.Map(location=[19.4326, -99.1332], zoom_start=11, tiles='CartoDB positron')

# Agregar denuncias por alcaldía
denuncias_por_alcaldia = df_filtrado['alcaldia_hecho'].value_counts().reset_index()
denuncias_por_alcaldia.columns = ['alcaldia', 'denuncias']
alcaldias_mapa = alcaldias.merge(denuncias_por_alcaldia, on='alcaldia', how='left')
alcaldias_mapa['denuncias'] = alcaldias_mapa['denuncias'].fillna(0)

# Colores por alcaldía
unique_alcaldias = alcaldias_mapa['alcaldia'].unique()
colors = plt.cm.tab20.colors
color_dict = {alcaldia: rgb2hex(colors[i % len(colors)]) for i, alcaldia in enumerate(unique_alcaldias)}

# Función de estilo
def style_function(feature):
    alcaldia = feature['properties']['alcaldia']
    return {
        'fillColor': color_dict.get(alcaldia, '#cccccc'),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.6
    }

# Capa GeoJSON
folium.GeoJson(
    alcaldias_mapa,
    name='Alcaldías',
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=['NOMGEO', 'denuncias'], aliases=['Alcaldía:', 'Denuncias:'])
).add_to(m)

# ------------------------
# Agregar marcadores
# ------------------------
color_marker = {'Adulto mayor': 'blue', 'General': 'red'}
for grupo in df_filtrado['grupo_poblacional'].unique():
    capa = folium.FeatureGroup(name=f"Población: {grupo}")
    for _, row in df_filtrado[df_filtrado['grupo_poblacional'] == grupo].iterrows():
        folium.CircleMarker(
            location=[row['latitud'], row['longitud']],
            radius=3,
            color=color_marker.get(grupo, 'gray'),
            fill=True,
            fill_opacity=0.5,
            popup=f"Delito: {row['delito']}<br>Alcaldía: {row['alcaldia_hecho']}<br>Hora: {row['hora_hecho']}"
        ).add_to(capa)
    capa.add_to(m)

# ------------------------
# Mostrar mapa
# ------------------------
folium.LayerControl().add_to(m)
folium_static(m, width=1000, height=700)
