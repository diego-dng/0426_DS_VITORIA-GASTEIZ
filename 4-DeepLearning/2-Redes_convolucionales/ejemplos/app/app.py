import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Satélite CNN", layout="centered")

st.title("Clasificador de Imágenes Satelitales")
st.write("Sube o arrastra una imagen satelital y nuestra Red Neuronal Convolucional adivinará qué hay en ella.")


@st.cache_resource
def cargar_modelo():
    return tf.keras.models.load_model('modelo/modelo_eurosat_cnn.keras')

modelo = cargar_modelo()

clases = [
    'AnnualCrop (Cultivo Anual)', 
    'Forest (Bosque)', 
    'HerbaceousVegetation (Veg. Herbácea)', 
    'Highway (Autopista)', 
    'Industrial (Zona Industrial)', 
    'Pasture (Pastizales)', 
    'PermanentCrop (Cultivo Permanente)', 
    'Residential (Zona Residencial)', 
    'River (Río)', 
    'SeaLake (Mar o Lago)'
]

archivo_subido = st.file_uploader("Arrastra aquí una imagen (.jpg, .jpeg, .png)", type=["jpg", "jpeg", "png"])

if archivo_subido is not None:
    
    imagen_pil = Image.open(archivo_subido).convert('RGB')
    st.image(imagen_pil, caption='Imagen a analizar', use_container_width=True)
    
    with st.spinner("La Red Neuronal está pensando... 🧠"):
        imagen_redimensionada = imagen_pil.resize((64, 64))
        img_array = np.array(imagen_redimensionada)
        
        img_array = img_array.astype('float32') / 255.0
        
        img_batch = np.expand_dims(img_array, axis=0)
        predicciones = modelo.predict(img_batch)[0]
        
        indice_ganador = np.argmax(predicciones)
        confianza = predicciones[indice_ganador] * 100
        clase_predicha = clases[indice_ganador]
        
        st.success(f"🎯 **Predicción Final:** {clase_predicha} (Seguridad: {confianza:.2f}%)")

        st.write("### Desglose de probabilidades:")
        
        fig, ax = plt.subplots(figsize=(8, 4))

        colores = ['#2e8b57' if i == indice_ganador else '#d3d3d3' for i in range(len(clases))]
        ax.barh(clases, predicciones * 100, color=colores)
        ax.set_xlabel('Probabilidad (%)')
        ax.set_xlim(0, 100) # El eje X va de 0 a 100%
        
        plt.gca().invert_yaxis() 
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        st.pyplot(fig)