import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm

def potencial_electrostatico():
    st.title("⚡ Potencial Electrostático de Carga Puntual")
    
    with st.expander("📚 Teoría", expanded=True):
        st.markdown("""
        **Potencial eléctrico de una carga puntual**:
        ```
        V = k·q/r
        ```
        Donde:
        - $k = 8.99×10^9\ N·m²/C²$ (Constante de Coulomb)
        - $q$: Carga [C]
        - $r$: Distancia desde la carga [m]
        """)
    
    col1, col2 = st.columns(2)
    with col1:
        q = st.slider("Carga (nC)", -20.0, 20.0, 10.0, 0.1)
    with col2:
        res = st.slider("Resolución", 100, 1000, 500, 50)
    
    # Constantes
    k_nano = 8.99e9 * 1e-9  # k para q en nC
    
    # Mallado
    x = np.linspace(-2, 2, res)
    y = np.linspace(-2, 2, res)
    X, Y = np.meshgrid(x, y)
    r = np.sqrt(X**2 + Y**2)
    r[r == 0] = 1e-10  # Evitar división por cero
    
    # Cálculo del potencial
    V = k_nano * q / r
    
    # Visualización
    fig, ax = plt.subplots(figsize=(10, 8))
    vmax = np.max(np.abs(V))
    linthresh = 0.1 * vmax
    
    # Mapa de color
    contour = ax.contourf(
        X, Y, V, 
        levels=100, 
        cmap='viridis',
        norm=SymLogNorm(linthresh=linthresh, linscale=1, vmin=-vmax, vmax=vmax))
    
    # Líneas equipotenciales
    ax.contour(X, Y, V, levels=12, colors='white', alpha=0.3, linewidths=0.5)
    
    # Carga puntual
    color = 'red' if q > 0 else 'blue'
    ax.scatter([0], [0], color=color, s=200, label=f'Carga: {q} nC')
    
    # Configuración
    cbar = plt.colorbar(contour, label='Potencial (V)')
    ax.set_title(f'Potencial {"Positivo" if q > 0 else "Negativo"}', pad=15)
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.legend()
    ax.grid(True, alpha=0.2)
    ax.set_aspect('equal')
    
    st.pyplot(fig)