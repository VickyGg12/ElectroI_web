import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d.proj3d import proj_transform

class Arrow3D(FancyArrowPatch):
    def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._xyz = (x, y, z)
        self._dxdydz = (dx, dy, dz)
    
    def draw(self, renderer):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)
        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        super().draw(renderer)
    
    def do_3d_projection(self, renderer=None):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)
        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return np.min(zs)

def simular_anillo_campo_electrico():
    st.title("🧲 Anillo con Distribución de Carga en Campo Eléctrico")
    
    with st.sidebar:
        st.header("Configuración de Parámetros")
        R = st.slider("Radio del anillo (m)", 0.05, 0.5, 0.1, 0.01)
        lambda0 = st.slider("Amplitud densidad de carga λ₀", 0.1, 5.0, 1.0, 0.1)
        E0 = st.slider("Campo eléctrico externo (N/C)", 0.1, 2.0, 0.5, 0.1)
    
    # Crear el anillo
    phi = np.linspace(0, 2*np.pi, 100)
    x_ring = R * np.cos(phi)
    y_ring = R * np.sin(phi)
    z_ring = np.zeros_like(phi)
    lambda_phi = lambda0 * np.sin(phi)

    # Cálculos físicos
    p_y = np.pi * lambda0 * R**2  # Momento dipolar
    tau_z = -p_y * E0  # Torque

    def add_arrow(ax, x, y, z, dx, dy, dz, label=None, mag=None, color='k', normalize=True, arrow_scale=1.0):
        if normalize:
            norm = np.sqrt(dx**2 + dy**2 + dz**2)
            if norm > 0:
                dx, dy, dz = dx/norm * R * arrow_scale, dy/norm * R * arrow_scale, dz/norm * R * arrow_scale
        arrow = Arrow3D(x, y, z, dx, dy, dz, color=color, arrowstyle='-|>', lw=2, mutation_scale=15)
        ax.add_artist(arrow)
        if label and mag is not None:
            ax.text(x + dx, y + dy, z + dz, f"{label}\n{mag:.4f}", color=color, fontsize=9)

    # Gráfico 3D
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Dibujar anillo con colores según densidad de carga
    sc = ax.scatter(x_ring, y_ring, z_ring, c=lambda_phi, cmap='bwr', alpha=0.9, s=20)
    cbar = fig.colorbar(sc, ax=ax, shrink=0.7, label='Densidad de carga λ(φ) [C/m]')

    # Campo eléctrico uniforme
    for y in np.linspace(-1.5*0.5, 1.5*0.5, 5):
        for z in np.linspace(-1.5*0.5, 1.5*0.5, 5):
            add_arrow(ax, -2*0.5, y, z, 2*0.5, 0, 0, color='#90EE90', normalize=True, arrow_scale=1)

    # Vectores de momento dipolar y torque
    add_arrow(ax, 0, 0, 0, 0, p_y, 0, label='p', mag=p_y, color='red', normalize=True, arrow_scale=3.0)
    add_arrow(ax, 0, 0, 0, 0, 0, tau_z, label='τ', mag=abs(tau_z), color='magenta', normalize=True, arrow_scale=3.0)

    # Leyenda
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='#90EE90', lw=2, label='Campo eléctrico (E)'),
        Line2D([0], [0], color='red', lw=2, label='Momento dipolar (p)'),
        Line2D([0], [0], color='magenta', lw=2, label='Torque (τ)')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    # Configuración del gráfico
    ax.set_xlim([-1, 0.4])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_xlabel('X [m]', fontsize=12)
    ax.set_ylabel('Y [m]', fontsize=12)
    ax.set_zlabel('Z [m]', fontsize=12)
    ax.set_title('Anillo con λ(φ)=λ₀sin(φ) en campo E externo\n' + r'$\vec{\tau} = \vec{p} \times \vec{E}$', fontsize=14)
    ax.grid(True, alpha=0.2)

    # Información física
    ax.text(-1, -1, 1.4,
            r'Magnitudes:' + '\n' +
            r'$|\vec{E}| = %.1f$ N/C' % E0 + '\n' +
            r'$|\vec{p}| = \pi \lambda_0 R^2 = %.4f$ C$\cdot$m' % p_y + '\n' +
            r'$|\vec{\tau}| = %.4f$ N$\cdot$m' % abs(tau_z) + '\n' +
            r'$R = %.2f$ m' % R,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

    st.pyplot(fig)
    
    # Explicación física
    with st.expander("📚 Explicación Física", expanded=True):
        st.markdown(f"""
        ### Física del Sistema:
        
        - **Distribución de carga**: λ(φ) = λ₀·sin(φ) - distribución sinusoidal alrededor del anillo
        - **Momento dipolar**: p⃗ = πλ₀R² ŷ = {p_y:.4f} C·m
        - **Torque**: τ⃗ = p⃗ × E⃗ = {tau_z:.4f} N·m en dirección z
        - **Radio del anillo**: R = {R} m
        
        ### Ecuaciones clave:
        ```
        p_y = π·λ₀·R²
        τ_z = -p_y·E₀
        ```
        
        El torque hace que el anillo tienda a alinearse con el campo eléctrico externo.
        """)

# Llamar la función
simular_anillo_campo_electrico()