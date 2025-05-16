
# Mapa Dinámico de Denuncias en CDMX

Este proyecto es una aplicación interactiva desarrollada con Streamlit que muestra un mapa dinámico y visualizaciones de denuncias en la Ciudad de México (CDMX). El mapa incluye puntos de denuncias clasificados por población, además de filtros para año, delito, día de la semana y franja horaria. También se visualizan estadísticas detalladas con gráficos para facilitar el análisis.

---

## Características

- Mapa de denuncias con puntos geolocalizados y diferenciados por grupo poblacional (adultos mayores y general).
- División por alcaldías con colores distintivos y leyendas claras.
- Filtros interactivos para seleccionar año, delitos, días de la semana y franjas horarias.
- Gráficos estadísticos interactivos para visualizar tendencias y distribución de denuncias.
- Aplicación desplegada en Streamlit para fácil acceso y uso.

---

## Archivos del proyecto

- `mapa_con_graficos.py`: Script principal que genera la app interactiva.
- `filtered_data.csv`: Dataset con las denuncias geolocalizadas y clasificadas.
- `alcaldias_cdmx.geojson`: Archivo geojson con los polígonos de las alcaldías de CDMX.
- `requirements.txt`: Lista de librerías necesarias para ejecutar la app.

---

## Requisitos

- Python 3.7 o superior
- Las librerías especificadas en `requirements.txt`

---

## Instalación y ejecución local

1. Clonar este repositorio:

```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio

Crear y activar un entorno virtual (opcional pero recomendado):
python -m venv env
source env/bin/activate   # En Windows: env\Scripts\activate


Instalar dependencias:
pip install -r requirements.txt


Ejecutar la aplicación:
streamlit run mapa_denuncias.py
