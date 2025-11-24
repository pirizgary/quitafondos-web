import streamlit as st
from rembg import remove
from PIL import Image
import io

# Configuración de página ancha
st.set_page_config(page_title="Quitafondos Pro", page_icon="🎨", layout="wide")

# --- AQUÍ ESTÁ EL CAMBIO: EL BANNER ---
try:
    # 1. Cargar la imagen (Asegúrate que el nombre coincida EXACTO con el de GitHub)
    banner_image = Image.open("banner.png") 
    
    # 2. Mostrarla (use_column_width=True hace que ocupe todo el ancho)
    st.image(banner_image, use_column_width=True)
except FileNotFoundError:
    # Si te olvidaste de subir la imagen, no se rompe la página, solo muestra un aviso discreto.
    st.warning("⚠️ No se encontró la imagen 'banner.png' en GitHub.")
# --------------------------------------

st.title("quitafondos fácil y sencillo")
st.write("Sube tu imagen y personaliza el resultado.")

# 1. Subir Imagen
uploaded_file = st.file_uploader("Sube tu foto aquí...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Dividimos en 2 columnas
    col1, col2 = st.columns([1, 1]) 
    
    # --- COLUMNA IZQUIERDA (FOTO) ---
    with col1:
        st.subheader("Tu Imagen")
        st.image(image, use_column_width=True)

    # --- COLUMNA DERECHA (CONTROLES) ---
    with col2:
        st.subheader("Configuración")
        
        # Paso 1: Elegir modo
        modo = st.radio(
            "Tipo de Fondo:",
            ["Transparente (PNG)", "Color Sólido"]
        )
        
        bg_color = None # Variable vacía por defecto
        
        if modo == "Color Sólido":
            # LISTA DE COLORES PREDEFINIDOS
            opciones_color = {
                "Blanco ⚪": "#FFFFFF",
                "Negro ⚫": "#000000",
                "Verde Chroma (Green Screen) 🟢": "#00FF00",
                "Rojo 🔴": "#FF0000",
                "Azul 🔵": "#0000FF",
                "Gris Profesional 🏢": "#808080",
                "Otro / Personalizado 🎨": "custom"
            }
            
            seleccion = st.selectbox("Elige un color rápido:", list(opciones_color.keys()))
            
            if opciones_color[seleccion] == "custom":
                bg_color = st.color_picker("Toca el recuadro para elegir color exacto:", "#5200FF")
            else:
                bg_color = opciones_color[seleccion]
        
        st.write("---")
        
        # Botón de Procesar
        if st.button("🚀 PROCESAR IMAGEN", type="primary"):
            with st.spinner('Trabajando la magia...'):
                try:
                    # A. Quitar fondo
                    img_procesada = remove(image)
                    
                    # B. Aplicar color si corresponde
                    if modo == "Color Sólido" and bg_color:
                        fondo_nuevo = Image.new("RGBA", img_procesada.size, bg_color)
                        img_procesada = Image.alpha_composite(fondo_nuevo, img_procesada)
                    
                    # C. Mostrar resultado
                    st.success("¡Imagen lista!")
                    st.image(img_procesada, caption='Resultado', use_column_width=True)
                    
                    # D. Descargar
                    buf = io.BytesIO()
                    img_procesada.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    st.download_button(
                        label="⬇️ Descargar Ahora",
                        data=byte_im,
                        file_name="imagen_editada.png",
                        mime="image/png"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")

