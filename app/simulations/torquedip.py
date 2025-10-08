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
    st.title("🧲 Torque sobre un Anillo con Densidad de Carga No Uniforme")
    
    with st.sidebar:
        st.header("Configuración de Parámetros")
        R = st.slider("Radio del anillo R (m)", 0.05, 0.5, 0.1, 0.01)
        lambda0 = st.slider("Amplitud densidad de carga λ₀ (C/m)", 0.1, 5.0, 1.0, 0.1)
        E0 = st.slider("Campo eléctrico externo E₀ (N/C)", 0.1, 2.0, 0.5, 0.1)
    
    # Cálculos físicos
    p_y = np.pi * lambda0 * R**2  # Momento dipolar
    tau_z = -p_y * E0  # Torque
    
    # Crear el anillo
    phi = np.linspace(0, 2*np.pi, 100)
    x_ring = R * np.cos(phi)
    y_ring = R * np.sin(phi)
    z_ring = np.zeros_like(phi)
    lambda_phi = lambda0 * np.sin(phi)

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
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Dibujar anillo con colores según densidad de carga
    sc = ax.scatter(x_ring, y_ring, z_ring, c=lambda_phi, cmap='bwr', alpha=0.9, s=30)
    cbar = fig.colorbar(sc, ax=ax, shrink=0.7, label='Densidad de carga λ(φ) [C/m]')
    cbar.ax.axhline(0, color='black', linestyle='--', alpha=0.5)  # Línea en cero

    # Campo eléctrico uniforme (flechas verdes)
    for y in np.linspace(-1.5*0.5, 1.5*0.5, 5):
        for z in np.linspace(-1.5*0.5, 1.5*0.5, 5):
            add_arrow(ax, -2*0.5, y, z, 2*0.5, 0, 0, color='#90EE90', normalize=True, arrow_scale=1)

    # Vectores físicos
    add_arrow(ax, 0, 0, 0, 0, p_y, 0, label='p⃗', mag=p_y, color='red', normalize=True, arrow_scale=3.0)
    add_arrow(ax, 0, 0, 0, 0, 0, tau_z, label='τ⃗', mag=abs(tau_z), color='magenta', normalize=True, arrow_scale=3.0)

    # Leyenda
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='#90EE90', lw=2, label='Campo eléctrico E⃗'),
        Line2D([0], [0], color='red', lw=2, label='Momento dipolar p⃗'),
        Line2D([0], [0], color='magenta', lw=2, label='Torque τ⃗'),
        Line2D([0], [0], color='blue', marker='o', lw=0, markersize=8, label='λ(φ) > 0'),
        Line2D([0], [0], color='red', marker='o', lw=0, markersize=8, label='λ(φ) < 0')
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

    # Información física en el gráfico
    ax.text(-1, -1, 1.4,
            r'Magnitudes:' + '\n' +
            r'$|\vec{E}| = %.1f$ N/C' % E0 + '\n' +
            r'$|\vec{p}| = \pi \lambda_0 R^2 = %.4f$ C$\cdot$m' % p_y + '\n' +
            r'$|\vec{\tau}| = %.4f$ N$\cdot$m' % abs(tau_z) + '\n' +
            r'$R = %.2f$ m' % R,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

    st.pyplot(fig)
    
    # Desarrollo matemático detallado
    with st.expander("📚 Desarrollo del problema", expanded=True):
        st.markdown("""
        ## **Torque sobre un anillo con densidad de carga no uniforme**

        ### **Definición de la distribución de carga**

        La densidad de carga lineal se define como una distribución sobre el espacio de funciones test $\\varphi \\in C^\\infty_c(\\mathbb{R}^3)$:

        $$
        \\langle \\lambda, \\varphi \\rangle = \\lambda_0 R \\int_0^{2\\pi} \\sin\\phi \\, \\varphi(R\\cos\\phi, R\\sin\\phi, 0) \\, \\mathrm{d}\\phi
        $$

        donde $\\lambda_0$ es la amplitud y $\\phi$ el ángulo azimutal. El anillo está parametrizado por $\\vec{r}(\\phi) = R(\\cos\\phi \\hat{x} + \\sin\\phi \\hat{y})$.

        ### **Momento dipolar eléctrico ($\\vec{p}$)**

        Para una distribución de carga, el momento dipolar es un funcional que actúa sobre funciones vectoriales de prueba $\\vec{\\psi} \\in [C^\\infty_c(\\mathbb{R}^3)]^3$:

        $$
        \\langle \\vec{p}, \\vec{\\psi} \\rangle = \\lambda_0 R^2 \\int_0^{2\\pi} \\sin\\phi \\, \\vec{\\psi}(R\\cos\\phi, R\\sin\\phi, 0) \\cdot (\\cos\\phi \\hat{x} + \\sin\\phi \\hat{y}) \\, \\mathrm{d}\\phi
        $$

        En el caso clásico (evaluando en $\\vec{\\psi} = \\mathbb{1}$):

        $$
        \\vec{p} = \\lambda_0 R^2 \\int_0^{2\\pi} \\sin\\phi (\\cos\\phi \\hat{x} + \\sin\\phi \\hat{y}) \\, \\mathrm{d}\\phi
        $$

        - **Componente $\\hat{x}$**:  
          $\\langle p_x, \\varphi \\rangle \\propto \\int \\sin\\phi \\cos\\phi \\, \\mathrm{d}\\phi = 0$ (integral de función impar en $[0, 2\\pi]$).
          
        - **Componente $\\hat{y}$**:  
          $\\langle p_y, \\varphi \\rangle = \\pi \\lambda_0 R^2 \\langle \\delta_y, \\varphi \\rangle$

        donde $\\delta_y$ es la distribución delta concentrada en el eje $y$. Así:

        $$
        \\vec{p} = \\pi \\lambda_0 R^2 \\, \\hat{y} \\quad [\\text{C·m}]
        $$

        ### **Torque ($\\vec{\\tau}$)**

        El campo eléctrico externo $\\vec{E} = E_0 \\hat{x}$ genera un torque:

        $$
        \\langle \\vec{\\tau}, \\vec{\\eta} \\rangle = -\\pi \\lambda_0 R^2 E_0 \\langle \\delta_z, \\eta_z \\rangle
        $$

        En forma vectorial:

        $$
        \\vec{\\tau} = -\\pi \\lambda_0 R^2 E_0 \\, \\hat{z} \\quad [\\text{N·m}]
        $$

        ### **Magnitudes físicas**
        \\begin{align*}
        |\\vec{E}| &= E_0 \\\\
        |\\vec{p}| &= \\pi \\lambda_0 R^2 \\\\
        |\\vec{\\tau}| &= \\pi \\lambda_0 R^2 E_0
        \\end{align*}
        """)

        # Mostrar valores numéricos
        st.markdown(f"""
        ### **Valores Numéricos para esta Simulación:**

        - **Radio del anillo**: $R = {R:.2f}$ m
        - **Amplitud de densidad de carga**: $\\lambda_0 = {lambda0:.1f}$ C/m
        - **Campo eléctrico externo**: $E_0 = {E0:.1f}$ N/C
        - **Momento dipolar calculado**: $|\\vec{{p}}| = \\pi \\times {lambda0:.1f} \\times ({R:.2f})^2 = {p_y:.4f}$ C·m
        - **Torque calculado**: $|\\vec{{\\tau}}| = {p_y:.4f} \\times {E0:.1f} = {abs(tau_z):.4f}$ N·m
        """)

    # Explicación física adicional
    with st.expander("🔍 Interpretación Física", expanded=True):
        st.markdown(f"""
        ### Física del Sistema:

        - **Distribución de carga**: $\\lambda(\\phi) = \\lambda_0\\cdot\\sin(\\phi)$ - distribución sinusoidal alrededor del anillo
        - **Momento dipolar**: $\\vec{{p}} = \\pi\\lambda_0 R^2 \\hat{{y}} = {p_y:.4f}$ C·m
        - **Torque**: $\\vec{{\\tau}} = \\vec{{p}} \\times \\vec{{E}} = {tau_z:.4f}$ N·m en dirección $\\hat{{z}}$
        - **Radio del anillo**: $R = {R}$ m

        ### Ecuaciones clave:
        ```
        p_y = π·λ₀·R²
        τ_z = -p_y·E₀
        ```

        ### Dirección del torque:
        El torque $\\vec{{\\tau}}$ apunta en la dirección $\\hat{{z}}$ negativa porque:
        - $\\vec{{p}}$ apunta en $+\\hat{{y}}$ (momento dipolar)
        - $\\vec{{E}}$ apunta en $+\\hat{{x}}$ (campo eléctrico)
        - $\\vec{{\\tau}} = \\vec{{p}} \\times \\vec{{E}} = p_y E_0 (\\hat{{y}} \\times \\hat{{x}}) = -p_y E_0 \\hat{{z}}$

        El torque hace que el anillo tienda a rotar para alinearse con el campo eléctrico externo.
        """)

        # Visualización de la regla de la mano derecha
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("**Regla de la mano derecha:**")
            st.markdown("""
            - Índice: $\\vec{p}$ (+ŷ)
            - Medio: $\\vec{E}$ (+ẋ)  
            - Pulgar: $\\vec{\\tau}$ (-ẑ)
            """)
        
        with col2:
            st.info("**Interpretación:**")
            st.markdown("""
            El torque hace rotar el anillo
            para alinear $\\vec{p}$ con $\\vec{E}$
            """)
        
        with col3:
            st.info("**Signo físico:**")
            st.markdown("""
            τ < 0 → rotación horaria
            vista desde +ẑ
            """)

# Llamar la función
simular_anillo_campo_electrico()