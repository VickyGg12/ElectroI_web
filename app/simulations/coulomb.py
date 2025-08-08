import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def calcular_fuerza(q1, q2, pos1, pos2):
    k = 8.9875e9  # Constante de Coulomb (N·m²/C²)
    r = pos2 - pos1
    distancia = np.linalg.norm(r)
    if distancia == 0:
        return np.zeros(2)

    fuerza_mag = k * np.abs(q1 * q2) / (distancia ** 2)
    fuerza_direc = r / distancia

    if q1 * q2 > 0:  # Repulsión
        fuerza_direc = -fuerza_direc
    else:             # Atracción
        fuerza_direc = fuerza_direc

    return fuerza_mag * fuerza_direc * 1e-11  # Escala para visualización

def mostrar_simulacion_coulomb():
    st.markdown("""
    <div class="simulation-container">
        <h3>Simulación interactiva de la Fuerza entre dos cargas</h3>
        <p>Utiliza los controles deslizantes para modificar las cargas y sus posiciones.</p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        q1 = st.slider(
            'Carga 1 (μC):',
            min_value=-5.0,
            max_value=5.0,
            value=1.0,
            step=0.1,  # Paso de 0.1 μC
            format="%.1f"  # Muestra 1 decimal
        )
        x1 = st.slider(
            'Posición 1 X (m):',
            min_value=-4.5,
            max_value=4.5,
            value=-2.0,
            step=0.1
        )
        y1 = st.slider(
            'Posición 1 Y (m):',
            min_value=-4.5,
            max_value=4.5,
            value=0.0,
            step=0.1
        )
    
    with col2:
        q2 = st.slider(
            'Carga 2 (μC):',
            min_value=-5.0,
            max_value=5.0,
            value=-1.0,
            step=0.1,
            format="%.1f"
        )
        x2 = st.slider(
            'Posición 2 X (m):',
            min_value=-4.5,
            max_value=4.5,
            value=2.0,
            step=0.1
        )
        y2 = st.slider(
            'Posición 2 Y (m):',
            min_value=-4.5,
            max_value=4.5,
            value=0.0,
            step=0.1
        )
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal')
    ax.grid(True)
    ax.set_title("Ley de Coulomb - Fuerza Electroestática")
    
    # Dibujar cargas
    carga1 = plt.Circle((x1, y1), 0.3, color='red' if q1 > 0 else 'blue', alpha=0.7, ec='black')
    carga2 = plt.Circle((x2, y2), 0.3, color='red' if q2 > 0 else 'blue', alpha=0.7, ec='black')
    ax.add_patch(carga1)
    ax.add_patch(carga2)
    
    # Calcular y dibujar fuerzas
    pos1 = np.array([x1, y1])
    pos2 = np.array([x2, y2])
    fuerza = calcular_fuerza(q1, q2, pos1, pos2)
    
    if np.any(fuerza):
        ax.arrow(pos1[0], pos1[1], fuerza[0], fuerza[1], 
                 head_width=0.3, head_length=0.5, fc='darkgreen', ec='darkgreen')
        ax.arrow(pos2[0], pos2[1], -fuerza[0], -fuerza[1], 
                 head_width=0.3, head_length=0.5, fc='darkgreen', ec='darkgreen')
    
    # Etiquetas
    ax.text(pos1[0], pos1[1]-0.5, f'q₁ = {q1:.1e} C', ha='center', 
            bbox=dict(facecolor='white', alpha=0.7, pad=2))
    ax.text(pos2[0], pos2[1]-0.5, f'q₂ = {q2:.1e} C', ha='center', 
            bbox=dict(facecolor='white', alpha=0.7, pad=2))
    
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)