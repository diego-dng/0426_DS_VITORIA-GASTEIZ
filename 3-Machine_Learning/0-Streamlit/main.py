import streamlit as st
import pickle

with open("modelos/modelo_prueba.pkl", "rb") as a:
    modelo = pickle.load(a)


# 	duracion	paginas	acciones	valor
# 0	7.0	        2	    4	        8	    
st.title("Prueba modelo")

st.write("Entorno para probar mi modelo")


with st.form(key ="formulario"):
    duracion = st.number_input("Duracion")
    paginas = st.number_input("Paginas")
    accion = st.number_input("Acciones")
    valor = st.number_input("Valor")


    boton = st.form_submit_button("Predecir")

if boton:
    
    #st.write(duracion)
    #st.write(paginas)
    #st.write(accion)
    #st.write(valor)
    datos = [[duracion, paginas, accion, valor]]
    st.write(datos)
    pred = modelo.predict(datos)

    if pred == "[0]":
        str_pred = "Windows"
    elif pred == "[1]":
        str_pred = "Linux"
    else:
        str_pred = "Mac"



    st.success(f"la predicción es: {str_pred}")
