import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle
from matplotlib.colors import LogNorm
from matplotlib.cm import ScalarMappable

class Arrow3D(plt.Line2D):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__([], [], *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_data(xs, ys)
        return min(zs)

def simular_campo_magnetico_bucle():
    st.title("🧭 Campo Magnético de un Bucle de Corriente")
    
    with st.sidebar:
        st.header("Configuración")
        I = st.slider("Corriente (A)", 0.1, 5.0, 1.0, 0.1)
        R = st.slider("Radio del bucle (m)", 0.05, 0.5, 0.1, 0.01)
        n_lines = st.slider("Número de líneas de campo", 8, 20, 12, 2)
    
    # Constantes
    mu0 = 4 * np.pi * 1e-7
    nano = 1e6

    def campo_bucle2(x, y, z):
        r = np.sqrt(x**2 + y**2 + z**2)
        m = I * np.pi * R**2
        prefactor = (mu0 * m) / (4 * np.pi) * nano

        Bx = prefactor * 3 * x * z / (r**5 + 1e-10)
        By = prefactor * 3 * y * z / (r**5 + 1e-10)
        Bz = prefactor * (3 * z**2 - r**2) / (r**5 + 1e-10)

        B_mag = np.sqrt(Bx**2 + By**2 + Bz**2)
        return Bx, By, Bz, B_mag

    # Crear figura
    fig = plt.figure(figsize=(16, 8))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 0.05])

    # Gráfico 3D
    ax1 = fig.add_subplot(gs[0], projection='3d')
    ax1.set_title(f"Campo magnético del bucle\nI = {I} A, R = {R} m", pad=20)

    # Dibujar bucle
    theta = np.linspace(0, 2*np.pi, 100)
    ax1.plot(R*np.cos(theta), R*np.sin(theta), np.zeros(100),
            'r-', lw=3, label='Bucle de corriente')

    # Parámetros para líneas de campo
    max_length = 25
    step_size = 0.1
    arrow_spacing = 6

    # Pre-calcular magnitudes para colormap
    all_B_mags = []
    phi = np.linspace(0, 2*np.pi, n_lines, endpoint=False)
    seeds = np.array([1.2*R*np.cos(phi), 1.2*R*np.sin(phi), 0.15*np.ones(n_lines)]).T

    for seed in seeds:
        pos = seed.copy()
        for _ in range(max_length):
            _, _, _, B_mag = campo_bucle2(pos[0], pos[1], pos[2])
            all_B_mags.append(B_mag)
            direction = np.array(campo_bucle2(pos[0], pos[1], pos[2])[:3])
            direction = direction / (np.linalg.norm(direction) + 1e-10)
            pos = pos + step_size * direction

    # Configurar colormap
    valid_B = np.array(all_B_mags)
    valid_B = valid_B[valid_B > 0]
    vmin_adjusted = max(valid_B.min() * 0.8, 0.05)
    vmax_adjusted = 13.0
    cmap = plt.get_cmap('gist_ncar')
    norm = LogNorm(vmin=vmin_adjusted, vmax=vmax_adjusted)

    # Dibujar líneas de campo
    for seed in seeds:
        trajectory = []
        B_mags = []

        # Integración
        pos = seed.copy()
        for _ in range(max_length):
            Bx, By, Bz, B_mag = campo_bucle2(pos[0], pos[1], pos[2])
            trajectory.append(pos.copy())
            B_mags.append(B_mag)
            direction = np.array([Bx, By, Bz])
            direction = direction / (np.linalg.norm(direction) + 1e-10)
            pos = pos + step_size * direction

        pos = seed.copy()
        for _ in range(max_length):
            Bx, By, Bz, B_mag = campo_bucle2(pos[0], pos[1], pos[2])
            trajectory.insert(0, pos.copy())
            B_mags.insert(0, B_mag)
            direction = np.array([Bx, By, Bz])
            direction = direction / (np.linalg.norm(direction) + 1e-10)
            pos = pos - step_size * direction

        trajectory = np.array(trajectory)
        B_mags = np.array(B_mags)

        # Dibujar línea
        for i in range(len(trajectory)-1):
            color_val = norm(min(B_mags[i], vmax_adjusted))
            ax1.plot(trajectory[i:i+2, 0], trajectory[i:i+2, 1], trajectory[i:i+2, 2],
                    color=cmap(color_val), lw=1.5, alpha=0.8)

    ax1.set_xlim(-0.8, 0.8)
    ax1.set_ylim(-0.8, 0.8)
    ax1.set_zlim(-0.8, 0.8)
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_zlabel('Z (m)')
    ax1.view_init(elev=30, azim=45)
    ax1.legend()
    ax1.grid(True, alpha=0.2)

    # Gráfico 2D
    ax2 = fig.add_subplot(gs[1])
    ax2.set_title(f"Sección del plano XZ\n∇·B = 0 (sin monopolos)", pad=20)

    # Crear mallado 2D
    x2d = np.linspace(-1.5, 1.5, 30)
    z2d = np.linspace(-1.5, 1.5, 30)
    X2d, Z2d = np.meshgrid(x2d, z2d)
    Y2d = np.zeros_like(X2d)

    Bx2d, By2d, Bz2d, B_mag2d = campo_bucle2(X2d, Y2d, Z2d)
    B_mag2d_clipped = np.clip(B_mag2d, vmin_adjusted, vmax_adjusted)

    # Streamplot
    strm = ax2.streamplot(X2d, Z2d, Bx2d, Bz2d, color=B_mag2d_clipped,
                         cmap=cmap, norm=norm, density=2, linewidth=1.5, arrowsize=1.2)

    # Bucle
    circle = Circle((0, 0), R, color='red', fill=False, lw=3)
    ax2.add_patch(circle)

    ax2.set_xlabel('X (m)')
    ax2.set_ylabel('Z (m)')
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.2)

    # Barra de color
    ax_cb = fig.add_subplot(gs[2])
    sm = ScalarMappable(norm=norm, cmap=cmap)
    cbar = fig.colorbar(sm, cax=ax_cb)
    cbar.set_label('Magnitud del campo (μT)', rotation=270, labelpad=20)

    plt.tight_layout()
    st.pyplot(fig)
    
    # Información adicional
    with st.expander("📊 Información del Campo Magnético"):
        m = I * np.pi * R**2
        st.markdown(f"""
        ### Parámetros del sistema:
        - **Corriente**: I = {I} A
        - **Radio del bucle**: R = {R} m
        - **Momento dipolar magnético**: m = I·π·R² = {m:.6f} A·m²
        - **Campo máximo cerca del bucle**: ~{vmax_adjusted} μT
        
        ### Características del campo:
        - **∇·B = 0**: No existen monopolos magnéticos
        - **Líneas cerradas**: El campo forma bucles cerrados
        - **Simetría axial**: Campo simétrico alrededor del eje Z
        """)

