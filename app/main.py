import streamlit as st
from simulations.coulomb import mostrar_simulacion_coulomb
from simulations.puntualfield import campo_electrico_carga_puntual
from simulations.potencial import potencial_electrostatico
from simulations.conductor import esfera_conductora
from simulations.hilosmag import campo_magnetico_hilos_interactivo
from simulations.BiotSavart import biot_savart_3d
from simulations.torquedip import simular_anillo_campo_electrico
from simulations.NoMonop import simular_campo_magnetico_bucle
from simulations.FibraOp import simular_fibra_optica_3d
from simulations.GuiaOnda import simular_guia_onda_mejorada
from simulations.RLC import simular_circuito_rlc

# Configuración de la página
st.set_page_config(
    page_title="Electromagnetismo I. Interactivo",
    page_icon="⚡",
    layout="wide"
)

# CSS mejorado y explicado
def load_css():
    st.markdown("""
    <style>
    /* Estilo principal para el contenedor */
    .main { 
        padding: 2rem; 
        background: linear-gradient(135deg, #f5f7fa 0%, #e4eaf1 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Cajas de bienvenida con sombra y bordes redondeados */
    .welcome-box {
        background-color: white;
        border-radius: 15px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        line-height: 1.6;
    }
    
    /* Espaciado para sliders */
    .stSlider { 
        margin: 15px 0; 
    }
    
    /* Tarjetas informativas con gradientes de color */
    .info-card {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 4px solid;
    }
    
    /* Variantes de colores para tarjetas */
    .card-blue {
        border-left-color: #003366;
        background: linear-gradient(135deg, #f0f8ff 0%, #e0f0ff 100%);
    }
    
    .card-red {
        border-left-color: #8b0000;
        background: linear-gradient(135deg, #fff0f5 0%, #ffeef0 100%);
    }
    
    /* Encabezado con gradiente azul */
    .header-gradient {
        background: linear-gradient(135deg, #003366 0%, #00509e 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    /* Estilos para encabezados */
    h1, h2, h3 {
        color: #2c5282 !important;
    }
    
    h4, h5 {
        color: #2c5282 !important;
    }
    
    /* Contenedor para logos */
    .logo-container {
        text-align: center;
        padding: 15px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    /* Pie de página */
    .footer {
        text-align: center;
        color: #666;
        font-size: 14px;
        margin-top: 30px;
        padding: 15px;
        border-top: 2px solid #e0e0e0;
    }
    
    /* Tamaño aumentado para emojis */
    .logo-emoji {
        font-size: 40px;
        margin-bottom: 10px;
    }
    
    </style>
    """, unsafe_allow_html=True)

load_css()

# Título principal
st.markdown("""
<div class="header-gradient">
    <h1 style="color: white; text-align: center; margin: 0;">📡 Material Didáctico de Electromagnetismo</h1>
    <p style="color: white; text-align: center; margin: 5px 0 0 0;">Facultad de Ciencias - UNAM</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Barra lateral con navegación
st.sidebar.title("⚡ Navegación")
seccion = st.sidebar.radio(
    "Selecciona un tema:",
    ["Inicio", "Electrostática", "Magnetostática", "Ondas Electromagnéticas", "Circuitos Eléctricos"]
)

# Contenido principal
if seccion == "Inicio":
    # Logos institucionales con emojis
    col1, col2, col3 = st.columns([1, 2, 1])
       
    with col1:
        # Escudo UNAM desde URL
        try:
            st.image("https://yosoycide.com/wp-content/uploads/2020/03/unam-escudo.png", 
                 width=100)
        except:
            st.info("No se pudo cargar el escudo UNAM")
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h2 style="color: #003366; margin-bottom: 10px;">🌟 Portal de Electromagnetismo</h2>
            <p style="font-size: 18px; color: #555;">Material didáctico interactivo</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Escudo Facultad de Ciencias desde URL
        try:
            st.image("https://iconape.com/wp-content/png_logo_vector/facultad-de-ciencias-unam-logo.png", 
                 width=100)
        except:
            st.info("No se pudo cargar el escudo de Facultad de Ciencias")
    
    # Separador
    st.markdown("---")
    
    # Información principal
    with st.container():
        st.markdown(
        """
        <style>
        .team-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 25px;
            border-radius: 12px;
            color: white;
            margin: 25px 0;
        }
        </style>
        """,
        unsafe_allow_html=True
        )
    
        st.markdown('<div class="team-box">', unsafe_allow_html=True)
        st.subheader("👥 Equipo de Desarrollo")
        st.markdown("**🧑‍💻 Desarrolladora:** Victoria González")
        st.markdown("**👨‍🏫 Asesores:** Dr. Mauricio García Vergara, Dra. Mirna Villavicencio Torres")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Sección de cómo usar la plataforma
    st.markdown("---")
    st.markdown("""
    <div class="welcome-box">
        <h4>🎯 ¿Cómo usar esta plataforma?</h4>
        <ol style="line-height: 1.8;">
            <li><strong>Selecciona un tema</strong> en el menú lateral izquierdo</li>
            <li><strong>Elige un subtema</strong> específico dentro de cada categoría</li>
            <li><strong>Interactúa</strong> con los controles deslizantes y parámetros</li>
            <li><strong>Observa</strong> cómo cambian las simulaciones en tiempo real</li>
            <li><strong>Experimenta</strong> con diferentes valores para comprender los conceptos</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer institucional
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p>🔬 Victoria Guevara González. Facultad de Ciencias - UNAM 🔭</p>
        <p>Hecho para la comunidad científica | © 2025 - Todos los derechos reservados</p>
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
    
    elif subtema == "Campos y potenciales eléctricos":
        tab1, tab2 = st.tabs(["📊 Potencial Eléctrico", "🧭 Campo Eléctrico"])
        with tab1:
            potencial_electrostatico()
        with tab2:
            campo_electrico_carga_puntual()
    
    elif subtema == "Conductores":
        st.subheader("🔗 Esfera Conductora")
        esfera_conductora()
    
    elif subtema == "Torque sobre una distribución de carga":
        st.info("Anillo con distribución de carga λ(φ)=λ₀·sin(φ)")
        simular_anillo_campo_electrico()
    
    elif subtema == "Energía electrostática":
        st.info("🚧 Simulación en desarrollo - Próximamente")
    
    elif subtema == "Desarrollo multipolar":
        st.info("🚧 Simulación en desarrollo - Próximamente")

elif seccion == "Magnetostática":
    st.header("🧲 Magnetostática")
    subtema = st.selectbox(
        "Selecciona un subtema:",
        ["Ley de Biot-Savart", "No existencia de monopolos magnéticos", 
         "Campo de inducción magnética"]
    )
    
    if subtema == "Ley de Biot-Savart":
        st.subheader("🔄 Ley de Biot-Savart en 3D")
        biot_savart_3d()
    
    elif subtema == "Campo de inducción magnética":
        st.subheader("🧵 Campo Magnético de Hilos Paralelos")
        campo_magnetico_hilos_interactivo()
    
    elif subtema == "No existencia de monopolos magnéticos":
        st.info("🧲 Campo Magnético de un Bucle de Corriente")
        simular_campo_magnetico_bucle()

elif seccion == "Ondas Electromagnéticas":
    st.header("🌊 Ondas Electromagnéticas")
    subtema = st.selectbox(
        "Selecciona un subtema:",
        ["Fibra óptica", "Guías de onda"]
    )
    
    if subtema == "Fibra óptica":
        st.subheader("〽️ Reflexión total interna para una fibra óptica")
        simular_fibra_optica_3d()

    elif subtema == "Guías de onda":
        st.subheader("📡 Guía de onda en TM y TE")
        simular_guia_onda_mejorada()

elif seccion == "Circuitos Eléctricos":
    st.header("🔌 Circuitos Eléctricos")
    subtema = st.selectbox(
        "Selecciona un subtema:",
        ["Circuitos RL, RC y RLC", "Leyes de Kirchhoff", "Teoremas de Thevenin y Norton"]
    )
    
    if subtema == "Circuitos RL, RC y RLC":
        st.subheader(" Simulación de Circuito RLC")
        simular_circuito_rlc()

    elif subtema == "Leyes de Kirchhoff":
        st.info("🚧 Simulación en desarrollo - Próximamente")
    
    elif subtema == "Teoremas de Thevenin y Norton":
        st.info("🚧 Simulación en desarrollo - Próximamente")
