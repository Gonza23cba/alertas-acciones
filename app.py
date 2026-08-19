import streamlit as st
import yfinance as yf
import pandas as pd
import ta
from datetime import datetime, timedelta
import time

# ============================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================

st.set_page_config(
    page_title="Señales de Trading",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# LISTA DE ACCIONES (ACTUALIZAR AQUÍ)
# ============================================

LISTA_ACCIONES = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META",
    "JPM", "V", "WMT", "PG", "KO", "PEP", "DIS", "NFLX",
    "XOM", "CVX", "BAC", "GS", "C", "AXP", "MA", "PYPL",
    "COIN", "SCHW", "BK", "BBVA", "SAN", "MELI", "NU", "XP",
]

NOMBRES_EMPRESAS = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corp.",
    "GOOGL": "Alphabet Inc.",
    "AMZN": "Amazon.com Inc.",
    "TSLA": "Tesla Inc.",
    "NVDA": "NVIDIA Corp.",
    "META": "Meta Platforms",
    "JPM": "JPMorgan Chase",
    "V": "Visa Inc.",
    "WMT": "Walmart Inc.",
    "PG": "Procter & Gamble",
    "KO": "Coca-Cola Co.",
    "PEP": "PepsiCo Inc.",
    "DIS": "Walt Disney Co.",
    "NFLX": "Netflix Inc.",
    "XOM": "Exxon Mobil Corp.",
    "CVX": "Chevron Corp.",
    "BAC": "Bank of America",
    "GS": "Goldman Sachs",
    "C": "Citigroup Inc.",
    "AXP": "American Express",
    "MA": "Mastercard Inc.",
    "PYPL": "PayPal Holdings",
    "COIN": "Coinbase Global",
    "SCHW": "Charles Schwab",
    "BK": "Bank of New York Mellon",
    "BBVA": "Banco Bilbao Vizcaya",
    "SAN": "Banco Santander",
    "MELI": "MercadoLibre Inc.",
    "NU": "Nu Holdings",
    "XP": "XP Inc.",
}

def get_nombre_empresa(simbolo):
    return NOMBRES_EMPRESAS.get(simbolo, simbolo)

# ============================================
# PARÁMETROS
# ============================================

dias_historia = 90
periodo_rapido = 21
periodo_lento = 30
INTERVALO_MINUTOS = 60  # Cada 60 minutos

# ============================================
# FUNCIONES
# ============================================

@st.cache_data(ttl=3600)
def obtener_datos(simbolo):
    try:
        ticker = yf.Ticker(simbolo)
        df = ticker.history(period=f"{dias_historia}d")
        if df.empty:
            return None
        return df
    except:
        return None

def calcular_soporte_resistencia(df):
    try:
        df_reciente = df.iloc[-30:]
        resistencia = df_reciente['High'].max()
        soporte = df_reciente['Low'].min()
        precio_actual = df['Close'].iloc[-1]
        distancia_resistencia = ((resistencia - precio_actual) / precio_actual) * 100
        distancia_soporte = ((precio_actual - soporte) / precio_actual) * 100
        return {
            'soporte': round(soporte, 2),
            'resistencia': round(resistencia, 2),
            'precio_actual': round(precio_actual, 2),
            'distancia_soporte': round(distancia_soporte, 2),
            'distancia_resistencia': round(distancia_resistencia, 2)
        }
    except:
        return None

def get_color_alerta(alerta):
    if any(palabra in alerta for palabra in ['ALCISTA', 'ROMPIÓ RESISTENCIA', 'GOLDEN']):
        return 'verde'
    elif any(palabra in alerta for palabra in ['BAJISTA', 'ROMPIÓ SOPORTE', 'DEATH']):
        return 'rojo'
    else:
        return 'amarillo'

def calcular_alertas(df, simbolo):
    alertas = []
    try:
        df['M21'] = df['Close'].rolling(window=periodo_rapido).mean()
        df['M30'] = df['Close'].rolling(window=periodo_lento).mean()
        
        macd = ta.trend.MACD(df['Close'])
        df['MACD'] = macd.macd()
        df['MACD_Signal'] = macd.macd_signal()
        
        ultimo = df.iloc[-1]
        anterior = df.iloc[-2]
        
        # ============================================
        # PRIORIDAD 1: CRUCE DE PRECIO vs MEDIAS
        # (Siempre primero)
        # ============================================
        if anterior['Close'] <= anterior['M21'] and ultimo['Close'] > ultimo['M21']:
            alertas.append(("PRECIO CRUZA M21 ALCISTA", 'verde', 1))
        elif anterior['Close'] >= anterior['M21'] and ultimo['Close'] < ultimo['M21']:
            alertas.append(("PRECIO CRUZA M21 BAJISTA", 'rojo', 1))
        
        if anterior['Close'] <= anterior['M30'] and ultimo['Close'] > ultimo['M30']:
            alertas.append(("PRECIO CRUZA M30 ALCISTA", 'verde', 1))
        elif anterior['Close'] >= anterior['M30'] and ultimo['Close'] < ultimo['M30']:
            alertas.append(("PRECIO CRUZA M30 BAJISTA", 'rojo', 1))
        
        # ============================================
        # PRIORIDAD 2: CRUCE ENTRE MEDIAS
        # ============================================
        if ultimo['M21'] > ultimo['M30'] and anterior['M21'] <= anterior['M30']:
            alertas.append(("GOLDEN CROSS (M21 > M30)", 'verde', 2))
        elif ultimo['M21'] < ultimo['M30'] and anterior['M21'] >= anterior['M30']:
            alertas.append(("DEATH CROSS (M21 < M30)", 'rojo', 2))
        
        # ============================================
        # PRIORIDAD 3: MACD
        # ============================================
        if ultimo['MACD'] > ultimo['MACD_Signal'] and anterior['MACD'] <= anterior['MACD_Signal']:
            alertas.append(("MACD ALCISTA", 'verde', 3))
        elif ultimo['MACD'] < ultimo['MACD_Signal'] and anterior['MACD'] >= anterior['MACD_Signal']:
            alertas.append(("MACD BAJISTA", 'rojo', 3))
        
        # ============================================
        # PRIORIDAD 4: SOPORTE/RESISTENCIA
        # ============================================
        niveles = calcular_soporte_resistencia(df)
        if niveles:
            precio_actual = niveles['precio_actual']
            if precio_actual > niveles['resistencia']:
                alertas.append(("ROMPIÓ RESISTENCIA", 'verde', 4))
            if precio_actual < niveles['soporte']:
                alertas.append(("ROMPIÓ SOPORTE", 'rojo', 4))
            if niveles['distancia_resistencia'] < 3 and niveles['distancia_resistencia'] > 0:
                alertas.append(("CERCA DE RESISTENCIA", 'amarillo', 4))
            if niveles['distancia_soporte'] < 3 and niveles['distancia_soporte'] > 0:
                alertas.append(("CERCA DE SOPORTE", 'amarillo', 4))
        
        # ============================================
        # ORDENAR POR PRIORIDAD (menor número primero)
        # ============================================
        alertas.sort(key=lambda x: x[2])
        
        # Convertir a formato final (sin el número de prioridad)
        alertas_final = [(texto, color) for texto, color, _ in alertas]
        
    except Exception as e:
        return None
    
    return alertas_final

# ============================================
# FUNCIÓN PRINCIPAL DE ANÁLISIS
# ============================================

def ejecutar_analisis():
    resultados = []
    for accion in LISTA_ACCIONES:
        df = obtener_datos(accion)
        if df is not None and not df.empty:
            alertas = calcular_alertas(df, accion)
            if alertas and len(alertas) > 0:
                resultados.append({
                    'accion': accion,
                    'nombre': get_nombre_empresa(accion),
                    'alertas': alertas,
                })
    return resultados

# ============================================
# INTERFAZ PRINCIPAL (SIN BANNER)
# ============================================

# --- INICIALIZAR SESSION STATE ---
if 'alertas_activas' not in st.session_state:
    st.session_state.alertas_activas = []
if 'ultima_actualizacion' not in st.session_state:
    st.session_state.ultima_actualizacion = None

# --- EJECUCIÓN AUTOMÁTICA ---
if (st.session_state.ultima_actualizacion is None or 
    (datetime.now() - st.session_state.ultima_actualizacion).total_seconds() > 3600):
    with st.spinner("Analizando acciones..."):
        st.session_state.alertas_activas = ejecutar_analisis()
        st.session_state.ultima_actualizacion = datetime.now()
    st.rerun()

# ============================================
# ESTADÍSTICAS + ÚLTIMA ACTUALIZACIÓN
# ============================================

total_acciones = len(LISTA_ACCIONES)
total_alertas = len(st.session_state.alertas_activas)

# Contar alertas alcistas y bajistas
verdes = 0
rojos = 0
for item in st.session_state.alertas_activas:
    for _, color in item['alertas']:
        if color == 'verde':
            verdes += 1
        elif color == 'rojo':
            rojos += 1

# Mostrar estadísticas en 4 columnas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Total Acciones", total_acciones, help="Acciones monitoreadas")
with col2:
    st.metric("🚨 Alertas Activas", total_alertas, help="Total de alertas generadas")
with col3:
    st.metric("🟢 Alcistas", verdes, help="Señales de compra", delta_color="normal")
with col4:
    st.metric("🔴 Bajistas", rojos, help="Señales de venta", delta_color="inverse")

# Última actualización (debajo de las estadísticas)
if st.session_state.ultima_actualizacion:
    st.caption(f"🔄 Última actualización: {st.session_state.ultima_actualizacion.strftime('%d/%m/%Y %H:%M:%S')}")
else:
    st.caption("🔄 Esperando primera actualización...")

st.markdown("---")

# ============================================
# MOSTRAR ALERTAS EN TARJETAS (4 POR FILA)
# ============================================

if st.session_state.alertas_activas:
    # CSS para las tarjetas
    st.markdown("""
    <style>
        .card-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-top: 20px;
        }
        .card-alcista {
            background: #ffffff;
            border: 3px solid #16a34a;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 2px 8px rgba(22, 163, 74, 0.15);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .card-alcista:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(22, 163, 74, 0.25);
        }
        .card-bajista {
            background: #ffffff;
            border: 3px solid #8b1a1a;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 2px 8px rgba(139, 26, 26, 0.15);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .card-bajista:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(139, 26, 26, 0.25);
        }
        .card-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 8px;
            border-bottom: 1px solid #f1f5f9;
            padding-bottom: 6px;
        }
        .card-title .ticker {
            font-size: 1.3rem;
            font-weight: 800;
        }
        .card-title .empresa {
            font-weight: 400;
            color: #475569;
            font-size: 0.85rem;
        }
        .card-alerta {
            font-size: 0.9rem;
            padding: 4px 0;
        }
        .card-alerta .verde {
            color: #16a34a;
            font-weight: 500;
        }
        .card-alerta .rojo {
            color: #8b1a1a;
            font-weight: 500;
        }
        .card-alerta .amarillo {
            color: #ca8a04;
            font-weight: 500;
        }
        @media (max-width: 1024px) {
            .card-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        @media (max-width: 600px) {
            .card-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # --- CONSTRUIR TODAS LAS TARJETAS EN UNA SOLA VARIABLE ---
    html_tarjetas = '<div class="card-grid">'
    
    for item in st.session_state.alertas_activas:
        accion = item['accion']
        nombre = item['nombre']
        alertas = item['alertas']
        
        # Determinar si tiene alertas bajistas
        tiene_bajista = any(color == 'rojo' for _, color in alertas)
        card_class = "card-bajista" if tiene_bajista else "card-alcista"
        
        # Construir la tarjeta
        html_tarjetas += f'<div class="{card_class}">'
        html_tarjetas += f'<div class="card-title"><span class="ticker">{accion}</span> · <span class="empresa">{nombre}</span></div>'
        
        for alerta_texto, color in alertas:
            color_class = "verde" if color == "verde" else "rojo" if color == "rojo" else "amarillo"
            emoji = "🟢" if color == "verde" else "🔴" if color == "rojo" else "🟡"
            html_tarjetas += f'<div class="card-alerta"><span class="{color_class}">{emoji} {alerta_texto}</span></div>'
        
        html_tarjetas += '</div>'
    
    html_tarjetas += '</div>'
    
    # Renderizar todas las tarjetas juntas
    st.markdown(html_tarjetas, unsafe_allow_html=True)

else:
    st.info("✅ No hay alertas activas en este momento. Todas las acciones están en estado neutral.")
