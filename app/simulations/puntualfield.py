import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import ScalarFormatter

def campo_electrico_carga_puntual():
    st.title("🏋️ Campo Eléctrico de Carga Puntual")
    
    # Teoría introductoria
    with st.expander("📚 Contexto", expanded=True):
        st.markdown("""
        
        """)
    
    # Controles interactivos
    col1, col2 = st.columns(2)
    with col1:
        q = st.slider(
            "Carga (nC)",
            min_value=-20.0,
            max_value=20.0,
            value=5.0,
            step=0.1,
            format="%.1f",
            help="Carga en nanocoulombs (1 nC = 10⁻⁹ C)"
        )
    with col2:
        grid_size = st.slider(
            "Resolución de malla",
            min_value=20,
            max_value=100,
            value=40,
            step=5
        )
    
    # Constante ajustada para nC
    k_nano = 8.99e9 * 1e-9  # k para q en nC y r en metros
    
    # ========== Cálculos ==========
    x = np.linspace(-2, 2, grid_size)
    y = np.linspace(-2, 2, grid_size)
    X, Y = np.meshgrid(x, y)
    r = np.sqrt(X**2 + Y**2)
    r[r == 0] = np.inf  # Evitar división por cero

    # Campo eléctrico
    Ex = k_nano * q * X / r**3
    Ey = k_nano * q * Y / r**3
    E_magnitude = np.sqrt(Ex**2 + Ey**2)
    
    # Normalización para visualización
    valid = E_magnitude > 0
    Ex_norm = np.zeros_like(Ex)
    Ey_norm = np.zeros_like(Ey)
    Ex_norm[valid] = Ex[valid] / E_magnitude[valid]
    Ey_norm[valid] = Ey[valid] / E_magnitude[valid]

    # ========== Visualización ==========
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Mapa de color logarítmico
    norm = LogNorm(vmin=E_magnitude[valid].min()*1.5, 
                   vmax=E_magnitude.max()*0.8)
    
    # Flechas del campo
    quiver = ax.quiver(
        X, Y, Ex_norm, Ey_norm, E_magnitude,
        cmap='nipy_spectral',
        norm=norm,
        scale=30,
        width=0.003,
        pivot='middle'
    )
    
    # Carga puntual
    charge_color = 'red' if q > 0 else 'blue'
    ax.scatter([0], [0], color=charge_color, s=300, 
               label=f'Carga: {q} nC', zorder=5)
    
    # Líneas equipotenciales
    V = k_nano * q / r
    ax.contour(X, Y, V, levels=12, colors='gray', alpha=0.4, linewidths=0.7)
    
    # Barra de color
    cbar = plt.colorbar(quiver, ax=ax, label='Magnitud del Campo (N/C)',
                       extend='both', shrink=0.8)
    cbar.formatter = ScalarFormatter()
    cbar.formatter.set_powerlimits((-2, 2))
    
    # Ajustes estéticos
    ax.set_title(f'Campo Eléctrico {"Positivo" if q > 0 else "Negativo"}', pad=15)
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.2)
    ax.set_aspect('equal')
    ax.set_xlim(-2.1, 2.1)
    ax.set_ylim(-2.1, 2.1)
    
    st.pyplot(fig)
    
    # Explicación adicional
    st.markdown("""
    ### 📝 Interpretación:
    - **Flechas**: Dirección y magnitud relativa del campo (color = intensidad).
    - **Líneas grises**: Superficies equipotenciales.
    - La densidad de flechas disminuye con el cuadrado de la distancia (ley de Coulomb).
    """)

# Llamada a la función
if __name__ == "__main__":
    campo_electrico_carga_puntual()