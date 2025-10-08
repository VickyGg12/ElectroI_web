import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def simular_guia_onda_mejorada():
    st.title("📡 Simulación de Guías de Onda Rectangulares")
    
    with st.sidebar:
        st.header("Configuración de Modos")
        a = st.slider("Ancho a (cm)", 1.0, 5.0, 2.0, 0.1)
        b = st.slider("Alto b (cm)", 0.5, 3.0, 1.0, 0.1)
        m = st.slider("Número de modo m", 0, 3, 1, 1)
        n = st.slider("Número de modo n", 0, 3, 0, 1)
        modo = st.selectbox("Tipo de modo", ['TE', 'TM'])
        frecuencia = st.slider("Frecuencia (GHz)", 1.0, 20.0, 10.0, 0.5)
    
    def calcular_campo_TE(x, y, a, b, m, n):
        X, Y = np.meshgrid(x, y)

        if m == 0 and n == 0:
            return np.zeros_like(X), np.zeros_like(X), np.zeros_like(X)

        Ex = (n/b) * np.cos(m * np.pi * X / a) * np.sin(n * np.pi * Y / b)
        Ey = (-m/a) * np.sin(m * np.pi * X / a) * np.cos(n * np.pi * Y / b)
        Ez = np.zeros_like(Ex)

        return Ex, Ey, Ez

    def calcular_campo_TM(x, y, a, b, m, n):
        X, Y = np.meshgrid(x, y)

        if m == 0 or n == 0:
            return np.zeros_like(X), np.zeros_like(X), np.zeros_like(X)

        Ex = (m/a) * np.cos(m * np.pi * X / a) * np.sin(n * np.pi * Y / b)
        Ey = (n/b) * np.sin(m * np.pi * X / a) * np.cos(n * np.pi * Y / b)
        Ez = np.sin(m * np.pi * X / a) * np.sin(n * np.pi * Y / b)

        return Ex, Ey, Ez

    def calcular_frecuencia_corte(a, b, m, n):
        c = 3e8
        a_m = a * 0.01
        b_m = b * 0.01
        return (c / 2) * np.sqrt((m / a_m)**2 + (n / b_m)**2) / 1e9

    # Crear malla
    x = np.linspace(0, a, 40)
    y = np.linspace(0, b, 40)
    X, Y = np.meshgrid(x, y)

    # Calcular campo
    if modo == 'TE':
        Ex, Ey, Ez = calcular_campo_TE(x, y, a, b, m, n)
        titulo_modo = f'TE{m}{n}'
        tipo_texto = 'TRANSVERSAL ELÉCTRICO (E₂ = 0, H₂ ≠ 0)'
    else:
        Ex, Ey, Ez = calcular_campo_TM(x, y, a, b, m, n)
        titulo_modo = f'TM{m}{n}'
        tipo_texto = 'TRANSVERSAL MAGNÉTICO (H₂ = 0, E₂ ≠ 0)'

    # Calcular frecuencia de corte
    fc = calcular_frecuencia_corte(a, b, m, n)

    # Magnitudes
    magnitud_transversal = np.sqrt(Ex**2 + Ey**2)
    magnitud_total = np.sqrt(Ex**2 + Ey**2 + Ez**2)

    # Normalizar
    Ex_norm = np.zeros_like(Ex)
    Ey_norm = np.zeros_like(Ey)
    valid = magnitud_transversal > 1e-10
    Ex_norm[valid] = Ex[valid] / magnitud_transversal[valid]
    Ey_norm[valid] = Ey[valid] / magnitud_transversal[valid]

    # Gráficos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Gráfico 1: Campo transversal
    im1 = ax1.contourf(X, Y, magnitud_transversal, levels=30, cmap='plasma', alpha=0.9)
    skip = 3
    ax1.quiver(X[::skip, ::skip], Y[::skip, ::skip],
              Ex_norm[::skip, ::skip], Ey_norm[::skip, ::skip],
              magnitud_transversal[::skip, ::skip],
              cmap='viridis', scale=25, width=0.005, pivot='middle', alpha=0.8)

    cbar1 = plt.colorbar(im1, ax=ax1, shrink=0.8)
    cbar1.set_label('Magnitud Campo Transversal (Eₓ, Eᵧ)')
    ax1.set_title(f'Campo Eléctrico Transversal - Modo {titulo_modo}\n{tipo_texto}')
    ax1.set_xlabel('x (cm)')
    ax1.set_ylabel('y (cm)')
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.2)

    # Gráfico 2: Campo longitudinal
    if modo == 'TM':
        im2 = ax2.contourf(X, Y, Ez, levels=30, cmap='RdBu_r', alpha=0.9)
        cbar2 = plt.colorbar(im2, ax=ax2, shrink=0.8)
        cbar2.set_label('Componente Longitudinal E₂')
        ax2.set_title(f'Campo Eléctrico Longitudinal - Modo {titulo_modo}\nE₂ ≠ 0')
    else:
        im2 = ax2.contourf(X, Y, np.zeros_like(Ex), levels=30, cmap='Greys', alpha=0.7)
        cbar2 = plt.colorbar(im2, ax=ax2, shrink=0.8)
        cbar2.set_label('Componente Longitudinal E₂')
        ax2.set_title(f'Campo Eléctrico Longitudinal - Modo {titulo_modo}\nE₂ = 0')
        ax2.text(0.5, 0.5, 'E₂ = 0\n(MODO TE)',
                transform=ax2.transAxes, ha='center', va='center',
                fontsize=14, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax2.set_xlabel('x (cm)')
    ax2.set_ylabel('y (cm)')
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.2)

    plt.tight_layout()
    st.pyplot(fig)
    
    # Información adicional
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        ### Información del Modo {titulo_modo}:
        
        **Dimensiones**: {a} × {b} cm  
        **Frecuencia**: {frecuencia:.1f} GHz  
        **Frecuencia corte**: {fc:.2f} GHz  
        
        **Estado**: {'✅ PROPAGACIÓN GUIADA' if frecuencia > fc else '❌ MODO EN CORTE'}
        """)
    
    with col2:
        st.info("""
        ### Explicación Física:
        
        **Modos TE**:
        - Campo eléctrico puramente transversal
        - Campo magnético tiene componente longitudinal
        - E₂ = 0, H₂ ≠ 0
        
        **Modos TM**:
        - Campo magnético puramente transversal  
        - Campo eléctrico tiene componente longitudinal
        - H₂ = 0, E₂ ≠ 0
        """)
