import streamlit as st
from rembg import remove
from PIL import Image
import io

# Título y diseño
st.set_page_config(page_title="Quitafondos", page_icon="✂️")
st.title("✂️ Removedor de Fondos")
st.write("Sube una foto y la Inteligencia Artificial hará el resto.")

# Subir archivo
uploaded_file = st.file_uploader("Elige una imagen (JPG o PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 1. Mostrar la imagen original
    image = Image.open(uploaded_file)
    
    # Creamos dos columnas para ver el "Antes" y "Después"
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Original")
        st.image(image, use_column_width=True)

    with col2:
        st.header("Sin Fondo")
        
        if st.button("✨ Quitar Fondo"):
            with st.spinner('Procesando... (esto puede tardar unos segundos)'):
                try:
                    # AQUÍ SUCEDE LA MAGIA
                    output = remove(image)
                    
                    # Mostramos el resultado
                    st.image(output, use_column_width=True)
                    
                    # Preparamos la descarga
                    # Convertimos la imagen a bytes en memoria (RAM)
                    buf = io.BytesIO()
                    output.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    # Botón de descarga
                    st.download_button(
                        label="⬇️ Descargar PNG",
                        data=byte_im,
                        file_name="imagen_sin_fondo.png",
                        mime="image/png"
                    )
                except Exception as e:
                    st.error(f"Hubo un error: {e}")