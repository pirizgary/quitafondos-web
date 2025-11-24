import streamlit as st
from rembg import remove
from PIL import Image
import io

# Configuración básica de la página
st.set_page_config(page_title="Editor de Fondos", page_icon="🎨")

# --- TRUCO CSS: OCULTAR MENÚS Y MARCAS DE AGUA ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# -------------------------------------------------

st.title(" Quitafondos gratuito")
st.write("Sube una foto, elige un color y transforma tu imagen.")

# 1. Subir Imagen
uploaded_file = st.file_uploader("Elige una imagen (JPG, PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Mostrar imagen original
    st.image(image, caption='Imagen Original', use_column_width=True)
    
    st.write("---")
    st.write("### ⚙️ Personalización")
    
    # 2. Selector de color
    bg_color = st.color_picker("Elige el color de fondo:", "#FFFFFF")
    
    if st.button("✨ Procesar Imagen"):
        with st.spinner('Trabajando en tu foto...'):
            try:
                # A. Quitar fondo
                img_sin_fondo = remove(image)
                
                # B. Poner color nuevo
                fondo_nuevo = Image.new("RGBA", img_sin_fondo.size, bg_color)
                imagen_final = Image.alpha_composite(fondo_nuevo, img_sin_fondo)
                
                # C. Mostrar resultado
                st.image(imagen_final, caption='Resultado Final', use_column_width=True)
                
                # D. Botón descarga
                buf = io.BytesIO()
                imagen_final.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="⬇️ Descargar Imagen Lista",
                    data=byte_im,
                    file_name="foto_editada.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")

# ... el resto de tu código ...


