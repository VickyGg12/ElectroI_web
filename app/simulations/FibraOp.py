import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def simular_fibra_optica_3d():
    st.title("🔦 Simulación 3D de Fibra Óptica - Reflexión Total Interna")
    
    with st.sidebar:
        st.header("Parámetros Ópticos")
        n_nucleo = st.slider("Índice refracción núcleo (n₁)", 1.4, 1.6, 1.5, 0.01)
        n_revestimiento = st.slider("Índice refracción revestimiento (n₂)", 1.3, 1.5, 1.4, 0.01)
        angulo_incidencia = st.slider("Ángulo de incidencia (°)", 0, 89, 45, 1)
        radio_nucleo = st.slider("Radio del núcleo (μm)", 3.0, 8.0, 5.0, 0.5)
        longitud_fibra = st.slider("Longitud de la fibra (μm)", 10.0, 30.0, 20.0, 2.0)
    
    def calcular_angulo_critico(n_nucleo, n_revestimiento):
        if n_nucleo <= n_revestimiento:
            return 90.0
        return np.degrees(np.arcsin(n_revestimiento / n_nucleo))
    
    def calcular_trayectoria_3d(n_nucleo, n_revestimiento, angulo_incidencia, radio_nucleo, longitud_fibra):
        angulo_critico = calcular_angulo_critico(n_nucleo, n_revestimiento)
        theta_i = np.radians(angulo_incidencia)
        
        # Punto inicial
        x, y, z = 0, -radio_nucleo * 0.8, 0
        trayectoria = [(x, y, z)]
        reflexiones = []
        
        # Vector dirección inicial
        direccion_xy = np.array([np.sin(theta_i), 0, np.cos(theta_i)])
        
        max_pasos = 20
        for paso in range(max_pasos):
            if z > longitud_fibra:
                break
                
            # Calcular intersección con la pared
            a = direccion_xy[0]**2 + direccion_xy[1]**2
            b = 2 * (x * direccion_xy[0] + y * direccion_xy[1])
            c = x**2 + y**2 - radio_nucleo**2
            
            discriminante = b**2 - 4 * a * c
            
            if discriminante < 0:
                break
                
            t = (-b - np.sqrt(discriminante)) / (2 * a)
            if t <= 0:
                t = (-b + np.sqrt(discriminante)) / (2 * a)
            
            x_nuevo = x + direccion_xy[0] * t
            y_nuevo = y + direccion_xy[1] * t
            z_nuevo = z + direccion_xy[2] * t
            
            if z_nuevo > longitud_fibra:
                t_final = (longitud_fibra - z) / direccion_xy[2]
                x_nuevo = x + direccion_xy[0] * t_final
                y_nuevo = y + direccion_xy[1] * t_final
                z_nuevo = longitud_fibra
                trayectoria.append((x_nuevo, y_nuevo, z_nuevo))
                break
            
            trayectoria.append((x_nuevo, y_nuevo, z_nuevo))
            
            # Verificar reflexión total interna
            if angulo_incidencia > angulo_critico:
                normal = np.array([x_nuevo, y_nuevo, 0])
                normal = normal / np.linalg.norm(normal)
                direccion_xy = direccion_xy - 2 * np.dot(direccion_xy, normal) * normal
                reflexiones.append((x_nuevo, y_nuevo, z_nuevo))
            else:
                break
            
            x, y, z = x_nuevo, y_nuevo, z_nuevo
        
        return np.array(trayectoria), reflexiones, angulo_critico
    
    # Calcular trayectoria
    trayectoria, reflexiones, angulo_critico = calcular_trayectoria_3d(
        n_nucleo, n_revestimiento, angulo_incidencia, radio_nucleo, longitud_fibra)
    
    # Crear figura 3D
    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Dibujar fibra óptica
    z_fibra = np.linspace(0, longitud_fibra, 50)
    theta = np.linspace(0, 2 * np.pi, 50)
    theta_grid, z_grid = np.meshgrid(theta, z_fibra)
    
    # Núcleo
    x_nucleo = radio_nucleo * np.cos(theta_grid)
    y_nucleo = radio_nucleo * np.sin(theta_grid)
    nucleo_surf = ax.plot_surface(x_nucleo, y_nucleo, z_grid, alpha=0.3, color='gold')
    
    # Revestimiento
    x_revest = radio_nucleo * 1.5 * np.cos(theta_grid)
    y_revest = radio_nucleo * 1.5 * np.sin(theta_grid)
    revest_surf = ax.plot_surface(x_revest, y_revest, z_grid, alpha=0.2, color='lightblue')
    
    # Bordes
    ax.plot(radio_nucleo * np.cos(theta), radio_nucleo * np.sin(theta), 0, 'b-', linewidth=2, alpha=0.7)
    ax.plot(radio_nucleo * np.cos(theta), radio_nucleo * np.sin(theta), longitud_fibra, 'b-', linewidth=2, alpha=0.7)
    
    # Trayectoria del rayo
    if len(trayectoria) > 1:
        ax.plot(trayectoria[:, 0], trayectoria[:, 1], trayectoria[:, 2], 'r-', linewidth=3, alpha=0.9)
        
        if reflexiones:
            reflexiones_arr = np.array(reflexiones)
            ax.scatter(reflexiones_arr[:, 0], reflexiones_arr[:, 1], reflexiones_arr[:, 2],
                      c='red', s=50, alpha=0.8)
    
    # Configuración 3D
    ax.set_xlabel('X (μm)', labelpad=15)
    ax.set_ylabel('Y (μm)', labelpad=15)
    ax.set_zlabel('Z (μm) - Dirección de propagación', labelpad=15)
    
    limit = radio_nucleo * 2
    ax.set_xlim([-limit, limit])
    ax.set_ylim([-limit, limit])
    ax.set_zlim([0, longitud_fibra])
    ax.view_init(elev=20, azim=45)
    
    # Información
    info_text = f'PARÁMETROS ÓPTICOS:\n\nn₁ = {n_nucleo:.3f}\nn₂ = {n_revestimiento:.3f}\nθ_crítico = {angulo_critico:.1f}°\nθ_incidencia = {angulo_incidencia}°\n\n'
    
    if angulo_incidencia > angulo_critico:
        info_text += f'✓ REFLEXIÓN TOTAL INTERNA\nReflexiones: {len(reflexiones)}'
        color = 'lightgreen'
    else:
        info_text += '✗ REFRACCIÓN\nPÉRDIDA POR RADIACIÓN'
        color = 'lightcoral'
    
    ax.text2D(0.02, 0.95, info_text, transform=ax.transAxes, fontsize=11,
             bbox=dict(boxstyle='round', facecolor=color, alpha=0.8))
    
    # Leyenda
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    legend_elements = [
        Patch(facecolor='gold', alpha=0.5, label='Núcleo (n₁)'),
        Patch(facecolor='lightblue', alpha=0.3, label='Revestimiento (n₂)'),
        Line2D([0], [0], color='blue', lw=2, alpha=0.7, label='Interfase'),
        Line2D([0], [0], color='red', lw=3, alpha=0.9, label='Trayectoria del rayo'),
        Line2D([0], [0], marker='o', color='red', markersize=8, label='Reflexión total', linestyle='None')
    ]
    
    ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1.05, 0.5))
    plt.tight_layout()
    
    st.pyplot(fig)
    
    # Explicación física
    with st.expander("📚 Principio de Reflexión Total Interna"):
        st.markdown(f"""
        ### Condición para reflexión total interna:
        
        **Ángulo crítico**: θ_c = arcsin(n₂/n₁) = {angulo_critico:.1f}°
        
        **Condición**: θ_incidencia > θ_c → {angulo_incidencia}° > {angulo_critico:.1f}°
        
        ### Ley de Snell:
        ```
        n₁·sin(θ₁) = n₂·sin(θ₂)
        ```
        
        Cuando θ₂ = 90°, ocurre reflexión total interna.
        
        **Resultado**: {'✅ CONFINAMIENTO DEL RAYO' if angulo_incidencia > angulo_critico else '❌ PÉRDIDA POR REFRACCIÓN'}
        """)

# Llamar la función
simular_fibra_optica_3d()