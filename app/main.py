import streamlit as st
from simulations.coulomb import mostrar_simulacion_coulomb
import os

# Configuración de la página
st.set_page_config(
    page_title="Electromagnetismo Interactivo",
    page_icon="⚡",
    layout="wide"
)

# CSS personalizado
def load_css():
    with open("app/static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Título principal
st.title("📡 Material Didáctico de Electromagnetismo")
st.markdown("---")

# Barra lateral con navegación
st.sidebar.title("⚡ Navegación")
seccion = st.sidebar.radio(
    "Selecciona un tema:",
    ["Inicio", "Electrostática", "Magnetostática", "Ondas Electromagnéticas", "Circuitos Eléctricos"]
)

# Contenido principal
if seccion == "Inicio":
    st.header("🌟 Bienvenido al Portal de Electromagnetismo")
    st.markdown("""
    <div class="welcome-box">
        Este sitio contiene material didáctico interactivo para el estudio del electromagnetismo a nivel licenciatura.
        <br><br>
        Utiliza el menú lateral para navegar entre los diferentes temas.
    </div>
    """, unsafe_allow_html=True)
    
elif seccion == "Electrostática":
    st.header("⚡ Electrostática")
    subtema = st.selectbox(
        "Selecciona un subtema:",
        ["Ley de Coulomb", "Campos y potenciales eléctricos", "Conductores", 
         "Energía electrostática", "Desarrollo multipolar"]
    )
    
    if subtema == "Ley de Coulomb":
        st.subheader("🔌 Simulación de la Ley de Coulomb")
        mostrar_simulacion_coulomb()
        
    # Agregar más subtemas...