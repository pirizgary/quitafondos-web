import streamlit as st
from rembg import remove
from PIL import Image
import io

st.set_page_config(page_title="Quitafondos", page_icon="✂️", layout="wide")

st.title("✂️ Quitafondos Mágico")
st.write("Sube tu imagen y elige cómo quieres descargarla.")

# 1. Subir Imagen
uploaded_file = st.file_uploader("Elige una imagen...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # --- AQUÍ ESTÁ EL CAMBIO ---
    # Dividimos la pantalla en 2 columnas
    col1, col2 = st.columns([1, 1]) 
    
    # COLUMNA IZQUIERDA: Solo la imagen
    with col1:
        st.subheader("Tu Imagen")
        # Al estar en una columna, la imagen se reduce automáticamente a la mitad
        st.image(image, use_column_width=True)

    # COLUMNA DERECHA: Los controles
    with col2:
        st.subheader("Configuración")
        
        # Opciones
        opcion = st.radio(
            "¿Cómo quieres el resultado?",
            ["Fondo Transparente (PNG)", "Fondo de Color"]
        )
        
        bg_color = None
        if opcion == "Fondo de Color":
            bg_color = st.color_picker("Elige el color:", "#00FF00")
        
        st.write("") # Un poco de espacio
        
        # Botón de Procesar (ahora está a la derecha, junto a la foto)
        if st.button("✨ PROCESAR AHORA", type="primary"):
            
            # --- PROCESAMIENTO ---
            with st.spinner('Trabajando...'):
                try:
                    # A. Quitar fondo
                    img_procesada = remove(image)
                    
                    # B. Poner color si es necesario
                    if opcion == "Fondo de Color" and bg_color:
                        fondo_nuevo = Image.new("RGBA", img_procesada.size, bg_color)
                        img_procesada = Image.alpha_composite(fondo_nuevo, img_procesada)
                    
                    # C. Mostrar el resultado (Debajo de las columnas o en la derecha)
                    st.success("¡Listo!")
                    st.image(img_procesada, caption='Resultado Final', use_column_width=True)
                    
                    # D. Descargar
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
