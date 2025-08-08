import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

def campo_magnetico_hilos_interactivo():
    st.title("🧲 Simulador Interactivo: Campos Magnéticos de dos Hilos de corriente")
    
    with st.expander("📚 Puedes manipular todos los parámetros", expanded=True):
        st.markdown("""
        Mostrar o no los campos individuales y el total, ajustar la resolución de la malla, y las posiciones y corrientes de los hilos.
        """)
    
    # Controles en sidebar
    with st.sidebar:
        st.header("Configuración de Hilos")
        col1, col2 = st.columns(2)
        with col1:
            x1 = st.slider("Hilo 1 - Pos X (m)", -2.0, 2.0, -0.5, 0.1)
            y1 = st.slider("Hilo 1 - Pos Y (m)", -2.0, 2.0, 0.0, 0.1)
            I1 = st.slider("Hilo 1 - Corriente (A)", -3.0, 3.0, 1.0, 0.1)
        with col2:
            x2 = st.slider("Hilo 2 - Pos X (m)", -2.0, 2.0, 0.5, 0.1)
            y2 = st.slider("Hilo 2 - Pos Y (m)", -2.0, 2.0, 0.0, 0.1)
            I2 = st.slider("Hilo 2 - Corriente (A)", -3.0, 3.0, 1.0, 0.1)
        
        st.markdown("---")
        show_individual = st.checkbox("Mostrar campos individuales", True)
        show_total = st.checkbox("Mostrar campo total", True)
        res = st.slider("Resolución de malla", 10, 30, 20)

    # Constantes
    mu0 = 4 * np.pi * 1e-7
    nano = 1e6  # Para convertir a μT

    # Funciones
    def campo_B(I, x0, y0, X, Y):
        r = np.sqrt((X - x0)**2 + (Y - y0)**2)
        Bx = -mu0 * I * (Y - y0) / (2 * np.pi * (r**2 + 1e-10)) * nano
        By = mu0 * I * (X - x0) / (2 * np.pi * (r**2 + 1e-10)) * nano
        return Bx, By, np.sqrt(Bx**2 + By**2)

    def normalize_arrows(Bx, By):
        norm = np.sqrt(Bx**2 + By**2)
        mask = norm > 0
        Bx_norm, By_norm = np.zeros_like(Bx), np.zeros_like(By)
        Bx_norm[mask] = Bx[mask] / norm[mask]
        By_norm[mask] = By[mask] / norm[mask]
        return Bx_norm, By_norm

    # Crear malla
    x_min, x_max = min(x1, x2)-1, max(x1, x2)+1
    y_min, y_max = min(y1, y2)-1, max(y1, y2)+1
    x = np.linspace(x_min, x_max, res)
    y = np.linspace(y_min, y_max, res)
    X, Y = np.meshgrid(x, y)

    # Calcular campos
    B1x, B1y, B1_mag = campo_B(I1, x1, y1, X, Y)
    B2x, B2y, B2_mag = campo_B(I2, x2, y2, X, Y)
    B_total_x, B_total_y = B1x + B2x, B1y + B2y
    B_total_mag = np.sqrt(B_total_x**2 + B_total_y**2)

    # Normalizar
    B1x_norm, B1y_norm = normalize_arrows(B1x, B1y)
    B2x_norm, B2y_norm = normalize_arrows(B2x, B2y)
    B_total_x_norm, B_total_y_norm = normalize_arrows(B_total_x, B_total_y)

    # Visualización
    fig, ax = plt.subplots(figsize=(10, 8))

    # Campos individuales (copper y winter_r)
    if show_individual:
        cmap1 = plt.cm.copper
        cmap2 = plt.cm.winter_r
        norm_max = max(B1_mag.max(), B2_mag.max())
        norm1 = Normalize(vmin=0, vmax=norm_max)
        norm2 = Normalize(vmin=0, vmax=norm_max)
        
        q1 = ax.quiver(X, Y, B1x_norm, B1y_norm, B1_mag,
                      cmap=cmap1, norm=norm1, scale=25, width=0.003, alpha=0.6)
        q2 = ax.quiver(X, Y, B2x_norm, B2y_norm, B2_mag,
                      cmap=cmap2, norm=norm2, scale=25, width=0.003, alpha=0.6)
        
        # Barras de color
        cbar1 = fig.colorbar(ScalarMappable(cmap=cmap1, norm=norm1), ax=ax, 
                            pad=0.02, shrink=0.4, aspect=10, location='left')
        cbar1.set_label('$|\mathbf{B}_1|$ (μT)', rotation=90)
        cbar2 = fig.colorbar(ScalarMappable(cmap=cmap2, norm=norm2), ax=ax, 
                            pad=0.02, shrink=0.4, aspect=10, location='right')
        cbar2.set_label('$|\mathbf{B}_2|$ (μT)', rotation=90)

    # Campo total (spring)
    if show_total:
        cmap_total = plt.cm.spring
        norm_total = Normalize(vmin=0, vmax=B_total_mag.max())
        
        q_total = ax.quiver(X, Y, B_total_x_norm, B_total_y_norm, B_total_mag,
                           cmap=cmap_total, norm=norm_total, scale=25, width=0.003)
        
        cbar_total = fig.colorbar(ScalarMappable(cmap=cmap_total, norm=norm_total), ax=ax,
                                 pad=0.02, shrink=0.4, aspect=10)
        cbar_total.set_label('$|\mathbf{B}_{total}|$ (μT)', rotation=270, labelpad=15)

    # Hilos y direcciones
    ax.plot(x1, y1, 'ro', markersize=12)
    ax.plot(x2, y2, 'bo', markersize=12)
    arrow_scale = 0.1 * max(abs(I1), abs(I2))
    ax.quiver(x1, y1, 0, np.sign(I1)*arrow_scale, color='red', scale=15, width=0.005)
    ax.quiver(x2, y2, 0, np.sign(I2)*arrow_scale, color='blue', scale=15, width=0.005)

    # Fuerzas
    force_scale = 0.3
    if I1 * I2 > 0:  # Atracción
        ax.arrow(x1, y1, (x2-x1)*force_scale, (y2-y1)*force_scale, 
                head_width=0.1, color='black')
        ax.arrow(x2, y2, (x1-x2)*force_scale, (y1-y2)*force_scale, 
                head_width=0.1, color='black')
    else:  # Repulsión
        ax.arrow(x1, y1, (x1-x2)*force_scale, (y1-y2)*force_scale, 
                head_width=0.1, color='black')
        ax.arrow(x2, y2, (x2-x1)*force_scale, (y2-y1)*force_scale, 
                head_width=0.1, color='black')

    # Configuración
    ax.set_title(f"Interacción entre Hilos\n$I_1$ = {I1} A, $I_2$ = {I2} A", pad=20)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_aspect('equal')

    # Leyenda
    handles = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
                  markersize=10, label=f'Hilo 1 ($I_1$ = {I1} A)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', 
                  markersize=10, label=f'Hilo 2 ($I_2$ = {I2} A)'),
        plt.Line2D([0], [0], color='black', lw=2, label='Fuerza')
    ]
    ax.legend(handles=handles, loc='upper right')

    st.pyplot(fig)
    

