import streamlit as st
from rembg import remove
from PIL import Image
import io

st.set_page_config(page_title="Quitafondos", page_icon="✂️")

st.title("✂️ Quitafondos Mágico")
st.write("Sube tu imagen y elige cómo quieres descargarla.")

# 1. Subir Imagen
uploaded_file = st.file_uploader("Elige una imagen...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Mostrar imagen original
    st.image(image, caption='Imagen Original', use_column_width=True)
    
    st.write("---")
    st.header("Configuración")
    
    # 2. PREGUNTA: ¿Qué tipo de fondo quieres?
    opcion = st.radio(
        "¿Cómo quieres el resultado final?",
        ["Fondo Transparente (PNG)", "Fondo de Color"]
    )
    
    # Si elige color, mostramos el selector. Si no, lo ocultamos.
    bg_color = None
    if opcion == "Fondo de Color":
        bg_color = st.color_picker("Elige el color:", "#00FF00")
    
    # 3. Botón de Procesar
    if st.button("✨ Realizar Magia"):
        with st.spinner('Procesando...'):
            try:
                # A. Quitamos el fondo (siempre se hace esto primero)
                img_procesada = remove(image)
                
                # B. Si eligió color, hacemos la fusión
                if opcion == "Fondo de Color" and bg_color:
                    # Creamos un fondo sólido del color elegido
                    fondo_nuevo = Image.new("RGBA", img_procesada.size, bg_color)
                    # Pegamos la imagen sin fondo encima del color
                    img_procesada = Image.alpha_composite(fondo_nuevo, img_procesada)
                
                # C. Mostrar resultado
                st.image(img_procesada, caption='Resultado Final', use_column_width=True)
                
                # D. Botón de descarga
                buf = io.BytesIO()
                img_procesada.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="⬇️ Descargar Imagen",
                    data=byte_im,
                    file_name="resultado.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"Hubo un error: {e}")
