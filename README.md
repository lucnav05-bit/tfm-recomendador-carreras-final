# Recomendador de Carreras/Estudios (TFM)

Este proyecto implementa un **sistema de recomendación de carreras y estudios** en función de intereses personales.  
La aplicación está desarrollada en **Streamlit** y utiliza un modelo de recomendación basado en contenido (**content-based**), donde se calculan perfiles promedio de cada carrera y se comparan con el perfil de cada usuario usando la **similitud coseno** (una métrica para medir semejanza entre vectores).

## Objetivos del proyecto
- Diseñar un prototipo de recomendación de estudios accesible y visual.  
- Implementar un cuestionario ampliado (36 ítems) que resume 12 dimensiones de interés.  
- Generar recomendaciones personalizadas de carreras en función de afinidad.  
- Explicar cada recomendación mediante los factores de interés más influyentes.  
- Ofrecer una interfaz sencilla para uso real (demo online).  

## Demo en línea
[Acceder a la aplicación en Streamlit](https://tfm-recomendador-carreras-final.streamlit.app/)

## Archivos del repositorio
- `app.py` → código de la aplicación en Streamlit  
- `requirements.txt` → librerías necesarias para ejecutar la app  
- `dataset_tfm_recomendacion_carreras.csv` → dataset sintético con usuarios, intereses y carreras  
- `README.md` → explicación y guía del proyecto  

## Vista previa de la aplicación
Ejemplo de cómo se ve la app funcionando:  

![Vista previa de la aplicación](screenshot_app.png)

## Uso local
Si quieres ejecutar el proyecto en tu propio ordenador:  

```bash
# Clona el repositorio
git clone https://github.com/lucnav05-bit/tfm-recomendador-carreras-final.git
cd tfm-recomendador-carreras-final

# Instala dependencias
pip install -r requirements.txt

# Ejecuta la app
streamlit run app.py


## Autora  
Lucía Gómez Navarro
Trabajo de fin de máster de Data Science, Big Data & Business Analytics de la Universidad Autónoma de Madrid 
