import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def simular_circuito_rlc():
    st.title("⚡ Simulación de Circuito RLC Serie")
    
    with st.sidebar:
        st.header("Parámetros del Circuito")
        R = st.slider("Resistencia R (Ω)", 1.0, 100.0, 10.0, 1.0)
        L = st.slider("Inductancia L (H)", 0.01, 1.0, 0.1, 0.01)
        C = st.slider("Capacitancia C (μF)", 1.0, 100.0, 10.0, 1.0)
        V0 = st.slider("Voltaje V₀ (V)", 1.0, 24.0, 12.0, 0.5)
        tipo_excitacion = st.selectbox("Tipo de excitación", ['escalon', 'senoidal', 'impulso'])
        
        if tipo_excitacion == 'senoidal':
            frecuencia = st.slider("Frecuencia (Hz)", 1.0, 1000.0, 60.0, 10.0)
        else:
            frecuencia = 60.0
    
    def ecuaciones_circuito(y, t, R, L, C, V0, tipo_excitacion, frecuencia):
        i, vc = y
        
        if tipo_excitacion == 'escalon':
            V_in = V0
        elif tipo_excitacion == 'senoidal':
            V_in = V0 * np.sin(2 * np.pi * frecuencia * t)
        else:  # impulso
            V_in = V0 if t < 1e-4 else 0
        
        di_dt = (V_in - R * i - vc) / L
        dvc_dt = i / C
        
        return [di_dt, dvc_dt]
    
    def calcular_parametros(R, L, C):
        omega0 = 1.0 / np.sqrt(L * C)
        f0 = omega0 / (2 * np.pi)
        alpha = R / (2 * L)
        zeta = alpha / omega0
        
        if zeta < 1:
            omega_d = omega0 * np.sqrt(1 - zeta**2)
        else:
            omega_d = 0
        
        return omega0, f0, alpha, zeta, omega_d
    
    # Convertir capacitancia de μF a F
    C_farad = C * 1e-6
    
    # Configurar tiempo de simulación
    if tipo_excitacion == 'escalon':
        t = np.linspace(0, 0.1, 1000)
    elif tipo_excitacion == 'senoidal':
        t = np.linspace(0, 0.05, 1000)
    else:  # impulso
        t = np.linspace(0, 0.02, 1000)
    
    # Condiciones iniciales
    y0 = [0.0, 0.0]
    
    try:
        # Resolver ecuaciones diferenciales
        sol = odeint(ecuaciones_circuito, y0, t,
                    args=(R, L, C_farad, V0, tipo_excitacion, frecuencia))
        
        i = sol[:, 0]
        vc = sol[:, 1]
        vr = R * i
        vl = L * np.gradient(i, t)
        
        # Calcular parámetros del circuito
        omega0, f0, alpha, zeta, omega_d = calcular_parametros(R, L, C_farad)
        
        # Gráficos
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Plot 1: Corriente
        ax1.plot(t * 1000, i * 1000, 'b-', linewidth=2)
        ax1.set_xlabel('Tiempo (ms)')
        ax1.set_ylabel('Corriente (mA)')
        ax1.set_title('Respuesta de Corriente $i(t)$')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Voltajes
        ax2.plot(t * 1000, vc, 'r-', linewidth=2, label='$V_C(t)$')
        ax2.plot(t * 1000, vr, 'g-', linewidth=2, label='$V_R(t)$')
        ax2.plot(t * 1000, vl, 'm-', linewidth=2, label='$V_L(t)$')
        ax2.set_xlabel('Tiempo (ms)')
        ax2.set_ylabel('Voltaje (V)')
        ax2.set_title('Voltajes en Componentes')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Energía
        energia_inductor = 0.5 * L * i**2 * 1000  # mJ
        energia_capacitor = 0.5 * C_farad * vc**2 * 1000  # mJ
        energia_total = energia_inductor + energia_capacitor
        
        ax3.plot(t * 1000, energia_inductor, 'c-', linewidth=2, label='Energía L')
        ax3.plot(t * 1000, energia_capacitor, 'y-', linewidth=2, label='Energía C')
        ax3.plot(t * 1000, energia_total, 'k--', linewidth=1, label='Energía Total')
        ax3.set_xlabel('Tiempo (ms)')
        ax3.set_ylabel('Energía (mJ)')
        ax3.set_title('Energía Almacenada')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Información
        ax4.axis('off')
        ax4.set_title('INFORMACIÓN DEL SISTEMA', fontweight='bold', pad=20)
        
        # Información con formato LaTeX
        info_text = 'PARÁMETROS DEL CIRCUITO:\n\n'
        info_text += f'$R = {R:.1f}\\ \\Omega$\n'
        info_text += f'$L = {L:.2f}\\ \\mathrm{{H}}$\n'
        info_text += f'$C = {C:.1f}\\ \\mu\\mathrm{{F}}$\n'
        info_text += f'$V_0 = {V0:.1f}\\ \\mathrm{{V}}$\n\n'
        
        info_text += 'PARÁMETROS CARACTERÍSTICOS:\n\n'
        info_text += f'$f_0 = {f0:.1f}\\ \\mathrm{{Hz}}$\n'
        info_text += f'$\\zeta = {zeta:.3f}$\n'
        info_text += f'$\\alpha = {alpha:.1f}\\ \\mathrm{{s^{{-1}}}}$\n\n'
        
        if zeta < 1:
            info_text += 'RESPUESTA: SUBAMORTIGUADA\n'
            info_text += f'$f_d = {omega_d/(2*np.pi):.1f}\\ \\mathrm{{Hz}}$'
            color = 'lightblue'
        elif abs(zeta - 1) < 0.01:
            info_text += 'RESPUESTA: CRÍTICAMENTE AMORTIGUADA'
            color = 'lightgreen'
        else:
            info_text += 'RESPUESTA: SOBREAMORTIGUADA'
            color = 'lightcoral'
        
        ax4.text(0.05, 0.85, info_text, transform=ax4.transAxes, fontsize=10,
                verticalalignment='top', 
                bbox=dict(boxstyle='round', facecolor=color, alpha=0.3))
        
        # Ecuaciones diferenciales
        eq_text = 'ECUACIONES DIFERENCIALES:\n\n'
        
        if tipo_excitacion == 'escalon':
            eq_text += 'Escalón: $V_{in} = V_0$\n\n'
        elif tipo_excitacion == 'senoidal':
            eq_text += f'Senoidal: $V_{{in}} = V_0 \\sin(2\\pi f t)$\n$f = {frecuencia}\\ \\mathrm{{Hz}}$\n\n'
        else:
            eq_text += 'Impulso: $V_{in} = V_0\\delta(t)$\n\n'
        
        eq_text += 'Sistema:\n'
        eq_text += '$L\\frac{di}{dt} + Ri + v_C = V_{in}$\n'
        eq_text += '$i = C\\frac{dv_C}{dt}$\n\n'
        
        eq_text += 'Ecuación de 2º orden:\n'
        eq_text += '$\\frac{d^2i}{dt^2} + 2\\alpha\\frac{di}{dt} + \\omega_0^2 i = \\frac{1}{L}\\frac{dV_{in}}{dt}$'
        
        ax4.text(0.55, 0.6, eq_text, transform=ax4.transAxes, fontsize=9,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
        
        plt.tight_layout()
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Error en la simulación: {e}")
        st.info("""
        **Solución de problemas:**
        - Verifica que los parámetros sean físicamente realistas
        - Reduce el paso de tiempo si hay problemas de convergencia
        - Asegúrate de que scipy esté instalado correctamente
        """)
    
    # Explicación adicional con LaTeX
    with st.expander("📚 Teoría del Circuito RLC", expanded=True):
        st.markdown("""
        ## Análisis del Circuito RLC Serie

        ### Ecuaciones Fundamentales

        **Sistema de ecuaciones diferenciales:**
        $$
        \\begin{align*}
        L\\frac{di}{dt} + Ri + v_C &= V_{in}(t) \\\\
        i &= C\\frac{dv_C}{dt}
        \\end{align*}
        $$

        **Ecuación diferencial de segundo orden para la corriente:**
        $$
        \\frac{d^2i}{dt^2} + 2\\alpha\\frac{di}{dt} + \\omega_0^2 i = \\frac{1}{L}\\frac{dV_{in}}{dt}
        $$

        ### Parámetros Característicos

        - **Frecuencia natural**: $\\omega_0 = \\frac{1}{\\sqrt{LC}}$
        - **Factor de amortiguamiento**: $\\alpha = \\frac{R}{2L}$
        - **Factor de amortiguamiento relativo**: $\\zeta = \\frac{\\alpha}{\\omega_0}$
        - **Frecuencia amortiguada**: $\\omega_d = \\omega_0\\sqrt{1-\\zeta^2}$ (si $\\zeta < 1$)

        ### Tipos de Respuesta

        1. **Subamortiguado** ($\\zeta < 1$):
           - Oscilaciones sinusoidales amortiguadas
           - $i(t) = A e^{-\\alpha t} \\sin(\\omega_d t + \\phi)$

        2. **Críticamente amortiguado** ($\\zeta = 1$):
           - Retorno más rápido a equilibrio sin oscilaciones
           - $i(t) = (A + Bt)e^{-\\alpha t}$

        3. **Sobreamortiguado** ($\\zeta > 1$):
           - Retorno lento a equilibrio sin oscilaciones
           - $i(t) = A e^{s_1 t} + B e^{s_2 t}$

        ### Energía en el Sistema

        - **Energía en el inductor**: $E_L = \\frac{1}{2}Li^2$
        - **Energía en el capacitor**: $E_C = \\frac{1}{2}Cv_C^2$
        - **Energía total**: $E_{total} = E_L + E_C$
        - **Potencia disipada**: $P_R = Ri^2$
        """)

