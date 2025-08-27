import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

def biot_savart_3d():
    st.title("🧭 Visualización 3D: Ley de Biot-Savart")
    
<<<<<<< HEAD
    # Sección histórica - FIEL AL ORIGINAL
    with st.expander("📚 Contexto Histórico (1820-1825)", expanded=True):
        st.markdown("""
        ### Construcción histórica de la Ley de Biot-Savart
        """)
        
        # Crear gráfico de línea de tiempo (FIEL AL ORIGINAL)
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
=======
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
>>>>>>> 421c61967f6d74fc8ef8f48ec351e9f4c23edd45
        plt.tight_layout()
        
        st.pyplot(fig_timeline)
    
    # Controles interactivos
    col1, col2 = st.columns(2)
    with col1:
        I = st.slider("Corriente (A)", 0.1, 5.0, 1.0, 0.1)
    with col2:
<<<<<<< HEAD
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
    
    ax_3d.plot(wire_x, wire_y, wire_z, 'b-', linewidth=3, label='Current-carrying wire')
    
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
    
    # Parámetros de la aguja (FIEL AL ORIGINAL)
    needle_pos = np.array([2.5, 2.5, 0])
    needle_length = 1.5
    
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
    
    # Calcular campo en todos los puntos
    B_fields = np.array([calculate_B(p) for p in obs_points])
    B_needle = calculate_B(needle_pos)
    
    # Dibujar líneas de campo (FIEL AL ORIGINAL)
    ax_3d.quiver(obs_points[:,0], obs_points[:,1], obs_points[:,2],
                 B_fields[:,0], B_fields[:,1], B_fields[:,2],
                 length=0.5, normalize=True, color='r', alpha=0.6)
    
    # Orientación de la brújula (FIEL AL ORIGINAL)
    if np.linalg.norm(B_needle) > 0:
        B_dir = B_needle/np.linalg.norm(B_needle)
    else:
        B_dir = np.array([1, 0, 0])
    
    needle_north = needle_pos + needle_length/2 * B_dir
    needle_south = needle_pos - needle_length/2 * B_dir
    
    # Dibujar la aguja (FIEL AL ORIGINAL)
    ax_3d.plot([needle_south[0], needle_north[0]],
               [needle_south[1], needle_north[1]],
               [needle_south[2], needle_north[2]],
               'g-', linewidth=4, label='Magnetic needle')
    
    # Crear base de la brújula (FIEL AL ORIGINAL)
    theta_circle = np.linspace(0, 2*np.pi, 100)
    compass_radius = 0.8
    x_circle = needle_pos[0] + compass_radius * np.cos(theta_circle)
    y_circle = needle_pos[1] + compass_radius * np.sin(theta_circle)
    z_circle = needle_pos[2] * np.ones_like(theta_circle)
    ax_3d.plot(x_circle, y_circle, z_circle, 'k-', linewidth=2, alpha=0.7)
    
    # Configuración del gráfico (FIEL AL ORIGINAL)
    ax_3d.set_box_aspect([1, 1, 1])
    ax_3d.set_xlim(-4, 4)
    ax_3d.set_ylim(-4, 4)
    ax_3d.set_zlim(-wire_length/2, wire_length/2)
    ax_3d.set_xlabel('X (m)')
    ax_3d.set_ylabel('Y (m)')
    ax_3d.set_zlabel('Z (m)')
    
    # Leyenda mejorada (FIEL AL ORIGINAL)
    legend_elements = [
        Line2D([0], [0], color='blue', lw=3, label='Cable conductor (corriente I)'),
        Line2D([0], [0], marker='>', color='blue', lw=0, label='Dirección de la corriente', markersize=10),
        Line2D([0], [0], color='red', lw=2, label='Campo magnético (B)'),
        Line2D([0], [0], color='green', lw=4, label='Aguja magnética')
=======
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
>>>>>>> 421c61967f6d74fc8ef8f48ec351e9f4c23edd45
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
<<<<<<< HEAD
    """)
=======
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
>>>>>>> 421c61967f6d74fc8ef8f48ec351e9f4c23edd45
