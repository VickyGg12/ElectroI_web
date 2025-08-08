import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

def campo_magnetico_hilos():
    st.title("🧵 Campo Magnético de Hilos de corriente")
    
    with st.expander("📚 Ley de Biot-Savart", expanded=True):
        st.markdown("""
        Puedes interactuar con los controles deslizantes para ajustar las corrientes y la separación entre los hilos.
        """)
    
    # Controles interactivos
    col1, col2 = st.columns(2)
    with col1:
        d = st.slider("Separación entre hilos (m)", 0.5, 3.0, 1.0, 0.1)
    with col2:
        I1 = st.slider("Corriente Hilo 1 (A)", -5.0, 5.0, 1.0, 0.1)
        I2 = st.slider("Corriente Hilo 2 (A)", -5.0, 5.0, 1.0, 0.1)
    
    # Constantes
    mu0 = 4 * np.pi * 1e-7
    nano = 1e6  # μT
    
    # Configuración
    wire1_pos = np.array([-d/2, 0])
    wire2_pos = np.array([d/2, 0])
    x = np.linspace(-2, 2, 20)
    y = np.linspace(-1.5, 1.5, 20)
    X, Y = np.meshgrid(x, y)
    
    # Funciones
    def campo_B(I, x0, y0):
        r = np.sqrt((X - x0)**2 + (Y - y0)**2)
        Bx = -mu0 * I * (Y - y0) / (2 * np.pi * r**2 + 1e-10) * nano
        By = mu0 * I * (X - x0) / (2 * np.pi * r**2 + 1e-10) * nano
        return Bx, By, np.sqrt(Bx**2 + By**2)
    
    # Cálculos
    B1x, B1y, B1_mag = campo_B(I1, *wire1_pos)
    B2x, B2y, B2_mag = campo_B(I2, *wire2_pos)
    B_total_x = B1x + B2x
    B_total_y = B1y + B2y
    B_total_mag = np.sqrt(B_total_x**2 + B_total_y**2)
    
    # Normalización
    def normalize(Bx, By):
        norm = np.sqrt(Bx**2 + By**2)
        mask = norm > 0
        Bx_norm, By_norm = np.zeros_like(Bx), np.zeros_like(By)
        Bx_norm[mask] = Bx[mask]/norm[mask]
        By_norm[mask] = By[mask]/norm[mask]
        return Bx_norm, By_norm
    
    # Visualización
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Flechas del campo
    skip = 2
    quiver = ax.quiver(
        X[::skip, ::skip], Y[::skip, ::skip],
        B_total_x[::skip, ::skip], B_total_y[::skip, ::skip],
        B_total_mag[::skip, ::skip],
        cmap='viridis', scale=30, width=0.004
    )
    
    # Hilos
    ax.plot(wire1_pos[0], wire1_pos[1], 'ro', markersize=12)
    ax.plot(wire2_pos[0], wire2_pos[1], 'bo', markersize=12)
    
    # Direcciones de corriente
    dir1 = 0.1 if I1 > 0 else -0.1
    dir2 = 0.1 if I2 > 0 else -0.1
    ax.quiver(wire1_pos[0], wire1_pos[1], 0, dir1, color='red', scale=15, width=0.005)
    ax.quiver(wire2_pos[0], wire2_pos[1], 0, dir2, color='blue', scale=15, width=0.005)
    
    # Configuración
    cbar = plt.colorbar(quiver, label='Magnitud del Campo (μT)')
    ax.set_title(f'Campo Magnético Total\n$I_1$ = {I1} A, $I_2$ = {I2} A')
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    st.pyplot(fig)