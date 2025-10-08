import streamlit as st # type: ignore
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from mpl_toolkits.mplot3d import Axes3D # type: ignore
from matplotlib.patches import Circle # type: ignore
from matplotlib.lines import Line2D # type: ignore

def biot_savart_3d():
    st.title("🧭 Visualización 3D: Ley de Biot-Savart")
    # Sección histórica
    with st.expander("📚 Contexto Histórico (1820-1825)", expanded=True):
        st.markdown("""
        ### Construcción histórica de la Ley de Biot-Savart
        """)
        
        # Crear gráfico de línea de tiempo
        fig_timeline, ax_timeline = plt.subplots(figsize=(12, 6))
        
        years = np.array([1820, 1821, 1823, 1824, 1825])
        events = [
            "Ørsted descubre efecto EM (aguja de una brújula se \nmueve al estar cerca de cable un largo)",
            "Ampère formula\n ley de fuerza entre dos corrientes",
            "Biot & Savart miden\ncampo magnético alrededor de un cable",
            "Laplace sugiera\nformulación matemática",
            "Ley de Biot-Savart\nes publicada"
        ]
        
        ax_timeline.plot(years, np.zeros_like(years), 'k-', marker='o', markersize=8)
        
        # Anotar los eventos (FIEL AL ORIGINAL)
        for year, event in zip(years, events):
            ax_timeline.annotate(event,
                         xy=(year, 0),
                         xytext=(0, 50 if year % 2 == 0 else -50),
                         textcoords='offset points',
                         ha='center', va='bottom' if year % 2 == 0 else 'top',
                         arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),
                         bbox=dict(boxstyle="round", fc="w", alpha=0.8))
        
        # Ilustración del experimento (FIEL AL ORIGINAL)
        ax_timeline.annotate("Arreglo experimental de Orsted:",
                     xy=(1822.5, -0.5), xytext=(1822.5, -2.5),
                     ha='center', va='top')
        
        ax_timeline.annotate("", xy=(1821, -3), xytext=(1824, -3),
                     arrowprops=dict(arrowstyle="<->"))
        ax_timeline.text(1822.5, -3.2, "Cable largo", ha='center')
        
        ax_timeline.annotate("", xy=(1823, -3.5), xytext=(1823, -4.5),
                     arrowprops=dict(arrowstyle="->"))
        ax_timeline.text(1823.2, -4, "Aguja magnética", ha='left')
        
        ax_timeline.annotate("", xy=(1823, -3.5), xycoords='data',
                     xytext=(1823.5, -2.5), textcoords='data',
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
        ax_timeline.text(1823.6, -2.5, "Dirección de la corriente", ha='left')
        
        # Formatting (FIEL AL ORIGINAL)
        ax_timeline.set_title("Construcción histórica de la Ley de Biot-Savart")
        ax_timeline.set_yticks([])
        ax_timeline.set_xticks(years, [str(year) for year in years])
        ax_timeline.set_xlim(1819, 1826)
        ax_timeline.set_ylim(-5, 3)
        ax_timeline.grid(True, axis='x', linestyle='--', alpha=0.5)
        plt.tight_layout()
        
        st.pyplot(fig_timeline)
    
    # Controles interactivos
    col1, col2 = st.columns(2)
    with col1:
        I = st.slider("Corriente (A)", 0.1, 5.0, 1.0, 0.1)
    with col2:
        wire_length = st.slider("Longitud cable (m)", 5, 20, 10, 1)
    
    # Constantes
    mu0 = 4 * np.pi * 1e-7
    nano = 1e6  # Para convertir a μT
    
    # Configuración 3D (FIEL AL ORIGINAL)
    fig_3d = plt.figure(figsize=(14, 10))
    ax_3d = fig_3d.add_subplot(111, projection='3d')
    ax_3d.set_title("Ley de Biot-Savart", pad=20, fontsize=14)
    
    # Parámetros del cable de corriente (FIEL AL ORIGINAL)
    num_segments = 100
    dz = wire_length / num_segments
    
    # Dibujar cable (FIEL AL ORIGINAL)
    wire_z = np.linspace(-wire_length/2, wire_length/2, num_segments)
    wire_x = np.zeros_like(wire_z)
    wire_y = np.zeros_like(wire_z)
    
    ax_3d.plot(wire_x, wire_y, wire_z, 'b-', linewidth=3, label='Cable conductor')
    
    # Dirección de la corriente (FIEL AL ORIGINAL)
    ax_3d.quiver(0, 0, wire_length/2-1, 0, 0, 2, color='blue',
              arrow_length_ratio=0.2, linewidth=2)
    ax_3d.text(0, 0, wire_length/2 + 1.5, "I", color='blue', fontsize=14)
    
    # Puntos en cilíndricas alrededor del bucle (FIEL AL ORIGINAL)
    theta = np.linspace(0, 2*np.pi, 20)
    r = np.linspace(0.5, 3, 3)
    obs_z_points = np.linspace(-wire_length/3, wire_length/3, 5)
    
    R, Theta, Z = np.meshgrid(r, theta, obs_z_points)
    obs_x = R * np.cos(Theta)
    obs_y = R * np.sin(Theta)
    obs_z = Z
    
    # Marcar estos puntos en el gráfico
    obs_points = np.vstack([obs_x.ravel(), obs_y.ravel(), obs_z.ravel()]).T
    
    # Función para calcular campo B (FIEL AL ORIGINAL)
    def calculate_B(point, max_segment=None):
        if max_segment is None:
            max_segment = num_segments

        B_total = np.zeros(3)
        for j in range(max_segment):
            segment = np.array([wire_x[j], wire_y[j], wire_z[j]])
            dl = np.array([0, 0, dz])

            r_vec = point - segment
            r_mag = np.linalg.norm(r_vec)

            if r_mag < 1e-6:
                continue

            dB = (mu0 * I / (4 * np.pi)) * np.cross(dl, r_vec) / (r_mag**3)
            B_total += dB

        # Normalizar y usar escala Log (FIEL AL ORIGINAL)
        B_mag = np.linalg.norm(B_total)
        if B_mag > 0:
            B_total = (B_total / nano) * np.log1p(B_mag/nano)
        return B_total
    
    # Calcular campo en todos los puntos (SOLO para los puntos de observación)
    B_fields = np.array([calculate_B(p) for p in obs_points])
    
    # Dibujar líneas de campo (FIEL AL ORIGINAL)
    ax_3d.quiver(obs_points[:,0], obs_points[:,1], obs_points[:,2],
                 B_fields[:,0], B_fields[:,1], B_fields[:,2],
                 length=0.5, normalize=True, color='r', alpha=0.6)
    
    # Configuración del gráfico (FIEL AL ORIGINAL)
    ax_3d.set_box_aspect([1, 1, 1])
    ax_3d.set_xlim(-4, 4)
    ax_3d.set_ylim(-4, 4)
    ax_3d.set_zlim(-wire_length/2, wire_length/2)
    ax_3d.set_xlabel('X (m)')
    ax_3d.set_ylabel('Y (m)')
    ax_3d.set_zlabel('Z (m)')
    
    # Leyenda mejorada (SIN la aguja magnética)
    legend_elements = [
        Line2D([0], [0], color='blue', lw=3, label='Cable conductor (corriente I)'),
        Line2D([0], [0], marker='>', color='blue', lw=0, label='Dirección de la corriente', markersize=10),
        Line2D([0], [0], color='red', lw=2, label='Campo magnético (B)')
    ]
    ax_3d.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    st.pyplot(fig_3d)
    
    # Explicación adicional
    st.markdown("""
    ### 📝 Interpretación:
    - **Cable azul**: Conductor rectilíneo con corriente $I$.
    - **Flechas rojas**: Dirección y sentido del campo magnético $\mathbf{B}$.
    - La intensidad del campo disminuye con la distancia al cable (ley inversa).
    - Las líneas de campo forman círculos concéntricos alrededor del cable.
    """)

