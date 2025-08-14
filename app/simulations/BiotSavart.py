import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

def biot_savart_3d():
    st.title("🧭 Visualización 3D: Ley de Biot-Savart")
    
    # Sección histórica
    with st.expander("📚 Contexto Histórico (1820-1825)", expanded=True):
        st.markdown("""
        ### Línea de tiempo del descubrimiento:
        """)
        
        # Crear gráfico de línea de tiempo
        fig_timeline, ax_timeline = plt.subplots(figsize=(10, 4))
        
        years = np.array([1820, 1821, 1823, 1824, 1825])
        events = [
            "Ørsted descubre efecto EM\n(aguja se mueve cerca de corriente)",
            "Ampère formula\nley de fuerza entre corrientes",
            "Biot & Savart miden\ncampo magnético",
            "Laplace sugiere\nformulación matemática",
            "Ley de Biot-Savart\nes publicada"
        ]
        
        ax_timeline.plot(years, np.zeros_like(years), 'k-o', markersize=8)
        
        for year, event in zip(years, events):
            y_offset = 0.5 if year % 2 == 0 else -0.5
            ax_timeline.annotate(event, xy=(year, 0), xytext=(0, 30*y_offset),
                               textcoords='offset points', ha='center',
                               bbox=dict(boxstyle='round', fc='w', alpha=0.8),
                               arrowprops=dict(arrowstyle="->"))
        
        # Configuración
        ax_timeline.set_title("Desarrollo Histórico de la Ley de Biot-Savart")
        ax_timeline.set_xlim(1819, 1826)
        ax_timeline.set_ylim(-1, 1)
        ax_timeline.axis('off')
        plt.tight_layout()
        
        st.pyplot(fig_timeline)
    
    # Controles interactivos
    col1, col2 = st.columns(2)
    with col1:
        I = st.slider("Corriente (A)", 0.1, 5.0, 1.0, 0.1)
    with col2:
        length = st.slider("Longitud cable (m)", 5, 20, 10, 1)
    
    # Configuración 3D
    fig_3d = plt.figure(figsize=(10, 8))
    ax_3d = fig_3d.add_subplot(111, projection='3d')
    
    # Dibujar cable conductor
    z_wire = np.linspace(-length/2, length/2, 100)
    ax_3d.plot(np.zeros_like(z_wire), np.zeros_like(z_wire), z_wire, 
              'b-', linewidth=3, label='Cable conductor')
    
    # Flecha para dirección de corriente
    ax_3d.quiver(0, 0, length/2-1, 0, 0, 2, 
                 color='blue', arrow_length_ratio=0.1, linewidth=2)
    ax_3d.text(0, 0, length/2 + 2, "I", color='blue', fontsize=14)
    
    # Puntos de observación (cilindro alrededor del cable)
    theta = np.linspace(0, 2*np.pi, 12)
    r = np.linspace(0.5, 3, 3)
    R, Theta = np.meshgrid(r, theta)
    obs_x = R * np.cos(Theta)
    obs_y = R * np.sin(Theta)
    obs_z = np.zeros_like(obs_x)
    
    # Calcular campo B en cada punto
    mu0 = 4e-7 * np.pi
    B_fields = []
    
    for x, y, z in zip(obs_x.ravel(), obs_y.ravel(), obs_z.ravel()):
        B = np.zeros(3)
        for z_seg in np.linspace(-length/2, length/2, 30):
            dl = np.array([0, 0, length/30])  # Elemento diferencial
            r_vec = np.array([x, y, z-z_seg])
            r_mag = np.linalg.norm(r_vec) + 1e-10
            
            # Ley de Biot-Savart
            dB = (mu0 * I / (4 * np.pi)) * np.cross(dl, r_vec) / (r_mag**3)
            B += dB
        
        # Normalizar para visualización
        B_norm = np.linalg.norm(B)
        if B_norm > 0:
            B = 0.5 * B / B_norm
        B_fields.append(B)
    
    B_fields = np.array(B_fields)
    
    # Visualización 3D del campo
    ax_3d.quiver(obs_x.ravel(), obs_y.ravel(), obs_z.ravel(),
                 B_fields[:,0], B_fields[:,1], B_fields[:,2],
                 length=0.8, color='red', alpha=0.8, label='Campo magnético')
    
    # Aguja magnética (brújula)
    needle_pos = np.array([2.5, 2.5, 0])
    B_needle = np.sum([calculate_B(needle_pos, z0) for z0 in np.linspace(-length/2, length/2, 30)], axis=0)
    if np.linalg.norm(B_needle) > 0:
        B_dir = B_needle / np.linalg.norm(B_needle)
    else:
        B_dir = np.array([1, 0, 0])
    
    needle_north = needle_pos + 1.0 * B_dir
    needle_south = needle_pos - 1.0 * B_dir
    
    ax_3d.plot([needle_south[0], needle_north[0]],
               [needle_south[1], needle_north[1]],
               [needle_south[2], needle_north[2]],
               'g-', linewidth=3, label='Aguja magnética')
    
    # Configuración del gráfico 3D
    ax_3d.set_xlim([-4, 4])
    ax_3d.set_ylim([-4, 4])
    ax_3d.set_zlim([-length/2-1, length/2+1])
    ax_3d.set_xlabel('X (m)')
    ax_3d.set_ylabel('Y (m)')
    ax_3d.set_zlabel('Z (m)')
    ax_3d.set_title("Campo Magnético alrededor de un Cable Rectilíneo")
    
    # Leyenda mejorada
    legend_elements = [
        Line2D([0], [0], color='blue', lw=3, label='Cable conductor'),
        Line2D([0], [0], marker='>', color='blue', lw=0, label='Corriente (I)', markersize=10),
        Line2D([0], [0], color='red', lw=2, label='Campo magnético (B)'),
        Line2D([0], [0], color='green', lw=3, label='Aguja magnética')
    ]
    ax_3d.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    st.pyplot(fig_3d)
    
    # Explicación adicional
    st.markdown("""
    ### 📝 Interpretación:
    - **Cable azul**: Conductor rectilíneo con corriente $I$.
    - **Flechas rojas**: Dirección y sentido del campo magnético $\mathbf{B}$.
    - **Aguja verde**: Brújula que se alinea con el campo magnético.
    - La intensidad del campo disminuye con la distancia al cable (ley inversa).
    """)

# Función auxiliar para calcular B en un punto
def calculate_B(point, z0, length=10, I=1.0, segments=30):
    mu0 = 4e-7 * np.pi
    dl = np.array([0, 0, length/segments])
    segment_pos = np.array([0, 0, z0])
    r_vec = point - segment_pos
    r_mag = np.linalg.norm(r_vec) + 1e-10
    return (mu0 * I / (4 * np.pi)) * np.cross(dl, r_vec) / (r_mag**3)