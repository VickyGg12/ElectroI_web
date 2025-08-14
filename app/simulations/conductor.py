import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def esfera_conductora():
    st.title("🧲 Esfera Conductora en Campo Eléctrico")
    
    with st.expander("📚 Teoría", expanded=True):
        st.markdown("""
        **Conductor en campo eléctrico externo**
        """)
    
    # Parámetros ajustables
    R = st.slider("Radio de la esfera (m)", 0.5, 2.0, 1.0, 0.1)
    E0 = st.slider("Campo externo (V/m)", 0.1, 5.0, 1.0, 0.1)
    
    # Mallado
    grid_size = 50
    plot_range = 3
    x = np.linspace(-plot_range, plot_range, grid_size)
    z = np.linspace(-plot_range, plot_range, grid_size)
    X, Z = np.meshgrid(x, z)
    
    # Cálculos
    r = np.sqrt(X**2 + Z**2)
    theta = np.arctan2(Z, X)
    
    V_outside = -E0*Z*(1 - (R**3)/(r**3))
    V = np.where(r >= R, V_outside, 0)
    
    # Visualización
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Potencial
    im = ax.pcolormesh(X, Z, V, shading='auto', cmap='nipy_spectral', alpha=0.8)
    cbar = plt.colorbar(im, label='Potencial (V)')
    
    # Líneas equipotenciales
    levels = np.linspace(-2.5*E0, 2.5*E0, 20)
    CS = ax.contour(X, Z, V, levels=levels, colors='white', linewidths=0.7)
    
    # Esfera
    ax.add_patch(Circle((0, 0), R, color='gray', alpha=0.6, label='Esfera conductora'))
    
    # Configuración
    ax.set_title('Distribución de Potencial')
    ax.set_xlabel('x (m)')
    ax.set_ylabel('z (m)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    st.pyplot(fig)
    