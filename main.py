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
# ESTILO PROFESIONAL MEJORADO
# ============================================

st.markdown("""
<style>
    /* FUENTE Y FONDO */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    .stApp {
        background: #f8fafc;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* ===== BANNER PRINCIPAL CON LOGO ===== */
    .main-banner {
        background: linear-gradient(135deg, #0d2818 0%, #1a3a2a 50%, #0f2a1a 100%);
        padding: 24px 32px;
        border-radius: 16px;
        margin-bottom: 28px;
        box-shadow: 0 4px 24px rgba(13, 40, 24, 0.25);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        border: 1px solid rgba(255,255,255,0.06);
    }
    
    .main-banner .logo-area {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    .main-banner .logo-text {
        display: flex;
        flex-direction: column;
        line-height: 1;
    }
    
    .main-banner .logo-text .senales {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    .main-banner .logo-text .detrading {
        font-size: 1.6rem;
        font-weight: 700;
        color: #4ade80;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: -4px;
    }
    
    .main-banner .badge-area {
        display: flex;
        align-items: center;
        gap: 16px;
        flex-wrap: wrap;
    }
    
    .main-banner .badge {
        background: rgba(255,255,255,0.08);
        color: #e2e8f0;
        padding: 6px 16px;
        border-radius: 40px;
        font-size: 0.75rem;
        border: 1px solid rgba(255,255,255,0.06);
        backdrop-filter: blur(4px);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .main-banner .badge .dot {
        width: 8px;
        height: 8px;
        background: #4ade80;
        border-radius: 50%;
        display: inline-block;
        animation: pulse-dot 2s infinite;
    }
    
    @keyframes pulse-dot {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.8); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    /* ===== ICONOS ALCISTA/BAJISTA ===== */
    .icono-alcista {
        display: inline-block;
        font-size: 1.2rem;
        margin-right: 6px;
    }
    .icono-bajista {
        display: inline-block;
        font-size: 1.2rem;
        margin-right: 6px;
    }
    
    /* ===== TARJETAS DE ESTADÍSTICAS ===== */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    }
    .stat-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 18px 22px;
        border: 1px solid #e9edf2;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        transition: all 0.2s;
    }
    .stat-card:hover {
        border-color: #cbd5e1;
    }
    .stat-card .label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .stat-card .value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 2px;
    }
    .stat-card .change {
        font-size: 0.8rem;
        font-weight: 500;
        color: #16a34a;
        background: #f0fdf4;
        padding: 2px 12px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 4px;
    }
    
    /* ===== SECCIÓN DE ALERTAS ===== */
    .section-alcistas {
        background: #f0fdf4;
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid #bbf7d0;
        margin-bottom: 16px;
    }
    .section-alcistas .section-title {
        color: #16a34a;
        font-weight: 700;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .section-bajistas {
        background: #fef2f2;
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid #fecaca;
        margin-bottom: 16px;
    }
    .section-bajistas .section-title {
        color: #dc2626;
        font-weight: 700;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .alerta-card {
        background: #ffffff;
        border-radius: 10px;
        padding: 12px 18px;
        border: 1px solid #e9edf2;
        margin-bottom: 8px;
        transition: all 0.15s;
        display: flex;
        align-items: center;
        gap: 12px;
        flex-wrap: wrap;
    }
    .alerta-card:hover {
        border-color: #cbd5e1;
        background: #fafcff;
    }
    .alerta-card .ticker {
        font-weight: 700;
        color: #0f172a;
        min-width: 70px;
        font-size: 0.95rem;
    }
    .alerta-card .empresa {
        color: #475569;
        font-size: 0.85rem;
        margin-right: 8px;
    }
    .alerta-card .mensaje {
        font-weight: 500;
        color: #0f172a;
        flex: 1;
        font-size: 0.9rem;
    }
    .alerta-card .badge-verde {
        background: #dcfce7;
        color: #16a34a;
        padding: 2px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
    }
    .alerta-card .badge-rojo {
        background: #fee2e2;
        color: #dc2626;
        padding: 2px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
    }
    .alerta-card .marketcap {
        color: #94a3b8;
        font-size: 0.7rem;
        font-weight: 500;
    }
    .alerta-card .icono-alerta {
        font-size: 1.1rem;
    }
    
    /* ===== BOTÓN ACTUALIZAR ===== */
    .stButton > button {
        background: #0f172a !important;
        color: white !important;
        font-weight: 500 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 28px !important;
        transition: all 0.2s !important;
        font-size: 0.9rem !important;
    }
    .stButton > button:hover {
        background: #1e293b !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.2) !important;
    }
    
    /* ===== ESTADO DE ACTUALIZACIÓN ===== */
    .update-status {
        background: #f1f5f9;
        border-radius: 8px;
        padding: 10px 18px;
        color: #475569;
        font-size: 0.85rem;
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
        border: 1px solid #e9edf2;
    }
    .update-status .dot-green {
        width: 10px;
        height: 10px;
        background: #22c55e;
        border-radius: 50%;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    .update-status .dot-gray {
        width: 10px;
        height: 10px;
        background: #94a3b8;
        border-radius: 50%;
        display: inline-block;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.4; }
        100% { opacity: 1; }
    }
    
    /* ===== FOOTER ===== */
    .footer {
        margin-top: 40px;
        padding: 20px 0 10px 0;
        border-top: 1px solid #e9edf2;
        text-align: center;
        color: #94a3b8;
        font-size: 0.75rem;
    }
    .footer strong {
        color: #475569;
    }
    .footer .disclaimer {
        color: #cbd5e1;
        font-size: 0.7rem;
        margin-top: 4px;
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .stats-grid { grid-template-columns: 1fr 1fr; }
        .main-banner { flex-direction: column; text-align: center; gap: 12px; }
        .main-banner .logo-area { flex-direction: column; }
        .main-banner .logo-text .senales { font-size: 1.8rem; }
        .main-banner .logo-text .detrading { font-size: 1.3rem; }
        .alerta-card { flex-direction: column; align-items: flex-start; gap: 4px; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# BANNER PRINCIPAL CON LOGO
# ============================================

st.markdown("""
<div class="main-banner">
    <div class="logo-area">
        <div class="logo-text">
            <span class="senales">📊 SENALES</span>
            <span class="detrading">DE TRADING</span>
        </div>
    </div>
    <div class="badge-area">
        <div class="badge">
            <span class="dot"></span>
            Mercado en vivo
        </div>
        <div class="badge">
            🔄 Actualización automática
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# LISTA DE ACCIONES (ACTUALIZAR AQUÍ)
# ============================================

# 🔥 ACTUALIZA ESTA LISTA CON TUS ACCIONES
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

@st.cache_data(ttl=3600)
def obtener_market_cap(simbolo):
    try:
        ticker = yf.Ticker(simbolo)
        info = ticker.info
        return info.get('marketCap', 0)
    except:
        return 0

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

def formatear_alerta(alerta):
    color = get_color_alerta(alerta)
    # No añadimos emoji aquí porque lo haremos después según la sección
    return alerta

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
        
        # --- PRIORIDAD 1: PRECIO vs MEDIAS ---
        if anterior['Close'] <= anterior['M21'] and ultimo['Close'] > ultimo['M21']:
            alertas.append(("PRECIO CRUZA M21 ALCISTA", 'verde'))
        elif anterior['Close'] >= anterior['M21'] and ultimo['Close'] < ultimo['M21']:
            alertas.append(("PRECIO CRUZA M21 BAJISTA", 'rojo'))
        
        if anterior['Close'] <= anterior['M30'] and ultimo['Close'] > ultimo['M30']:
            alertas.append(("PRECIO CRUZA M30 ALCISTA", 'verde'))
        elif anterior['Close'] >= anterior['M30'] and ultimo['Close'] < ultimo['M30']:
            alertas.append(("PRECIO CRUZA M30 BAJISTA", 'rojo'))
        
        # --- PRIORIDAD 2: CRUCE ENTRE MEDIAS ---
        if ultimo['M21'] > ultimo['M30'] and anterior['M21'] <= anterior['M30']:
            alertas.append(("GOLDEN CROSS (M21 > M30)", 'verde'))
        elif ultimo['M21'] < ultimo['M30'] and anterior['M21'] >= anterior['M30']:
            alertas.append(("DEATH CROSS (M21 < M30)", 'rojo'))
        
        # --- PRIORIDAD 3: MACD ---
        if ultimo['MACD'] > ultimo['MACD_Signal'] and anterior['MACD'] <= anterior['MACD_Signal']:
            alertas.append(("MACD ALCISTA", 'verde'))
        elif ultimo['MACD'] < ultimo['MACD_Signal'] and anterior['MACD'] >= anterior['MACD_Signal']:
            alertas.append(("MACD BAJISTA", 'rojo'))
        
        # --- PRIORIDAD 4: SOPORTE/RESISTENCIA ---
        niveles = calcular_soporte_resistencia(df)
        if niveles:
            precio_actual = niveles['precio_actual']
            if precio_actual > niveles['resistencia']:
                alertas.append(("ROMPIÓ RESISTENCIA", 'verde'))
            if precio_actual < niveles['soporte']:
                alertas.append(("ROMPIÓ SOPORTE", 'rojo'))
            if niveles['distancia_resistencia'] < 3 and niveles['distancia_resistencia'] > 0:
                alertas.append(("CERCA DE RESISTENCIA", 'amarillo'))
            if niveles['distancia_soporte'] < 3 and niveles['distancia_soporte'] > 0:
                alertas.append(("CERCA DE SOPORTE", 'amarillo'))
        
    except Exception as e:
        return None
    
    return alertas

def formatear_market_cap(market_cap):
    if market_cap >= 1_000_000_000_000:
        return f"${market_cap / 1_000_000_000_000:.2f}T"
    elif market_cap >= 1_000_000_000:
        return f"${market_cap / 1_000_000_000:.2f}B"
    elif market_cap >= 1_000_000:
        return f"${market_cap / 1_000_000:.2f}M"
    else:
        return f"${market_cap:,}"

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
                market_cap = obtener_market_cap(accion)
                resultados.append({
                    'accion': accion,
                    'nombre': get_nombre_empresa(accion),
                    'alertas': alertas,  # lista de (texto, color)
                    'market_cap': market_cap
                })
    resultados.sort(key=lambda x: x['market_cap'], reverse=True)
    return resultados

# ============================================
# INTERFAZ PRINCIPAL
# ============================================

# --- INICIALIZAR SESSION STATE ---
if 'alertas_activas' not in st.session_state:
    st.session_state.alertas_activas = []
if 'ultima_actualizacion' not in st.session_state:
    st.session_state.ultima_actualizacion = None

# --- BOTÓN DE ACTUALIZACIÓN MANUAL ---
col1, col2 = st.columns([4, 1])
with col1:
    if st.session_state.ultima_actualizacion:
        st.markdown(f"""
        <div class="update-status">
            <span class="dot-green"></span>
            Última actualización: {st.session_state.ultima_actualizacion.strftime('%d/%m/%Y %H:%M:%S')}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="update-status">
            <span class="dot-gray"></span>
            Esperando primera actualización...
        </div>
        """, unsafe_allow_html=True)

with col2:
    if st.button("🔄 Actualizar ahora"):
        with st.spinner("Analizando acciones..."):
            st.session_state.alertas_activas = ejecutar_analisis()
            st.session_state.ultima_actualizacion = datetime.now()
        st.rerun()

# --- EJECUCIÓN AUTOMÁTICA ---
if (st.session_state.ultima_actualizacion is None or 
    (datetime.now() - st.session_state.ultima_actualizacion).total_seconds() > 3600):
    with st.spinner("Analizando acciones..."):
        st.session_state.alertas_activas = ejecutar_analisis()
        st.session_state.ultima_actualizacion = datetime.now()
    st.rerun()

# --- ESTADÍSTICAS ---
total_acciones = len(LISTA_ACCIONES)
total_alertas = len(st.session_state.alertas_activas)

# Contar tipos de alertas
verdes = 0
rojos = 0
amarillos = 0
for item in st.session_state.alertas_activas:
    for _, color in item['alertas']:
        if color == 'verde':
            verdes += 1
        elif color == 'rojo':
            rojos += 1
        else:
            amarillos += 1

st.markdown(f"""
<div class="stats-grid">
    <div class="stat-card">
        <div class="label">📊 Total Acciones</div>
        <div class="value">{total_acciones}</div>
        <div class="change">Monitoreadas</div>
    </div>
    <div class="stat-card">
        <div class="label">🚨 Alertas Activas</div>
        <div class="value" style="color: {'#0f172a' if total_alertas > 0 else '#94a3b8'};">{total_alertas}</div>
        <div class="change">{'⚠️ Hay señales' if total_alertas > 0 else '✅ Sin alertas'}</div>
    </div>
    <div class="stat-card">
        <div class="label">🟢 Alcistas</div>
        <div class="value" style="color: #16a34a;">{verdes}</div>
        <div class="change">Señales de compra</div>
    </div>
    <div class="stat-card">
        <div class="label">🔴 Bajistas</div>
        <div class="value" style="color: #dc2626;">{rojos}</div>
        <div class="change">Señales de venta</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# MOSTRAR ALERTAS SEPARADAS
# ============================================

st.markdown("---")

# --- SEPARAR ALERTAS POR TIPO ---
alertas_alcistas = []
alertas_bajistas = []

for item in st.session_state.alertas_activas:
    alcistas_item = []
    bajistas_item = []
    for alerta_texto, color in item['alertas']:
        if color == 'verde':
            alcistas_item.append(alerta_texto)
        elif color == 'rojo':
            bajistas_item.append(alerta_texto)
        # Las amarillas las mostramos en la sección de alcistas o bajistas según contexto
        # Por ahora las dejamos en una sección separada o las incluimos en alcistas
        elif color == 'amarillo':
            alcistas_item.append(alerta_texto)  # Las ponemos en alcistas como neutras
    
    if alcistas_item:
        alertas_alcistas.append({
            'accion': item['accion'],
            'nombre': item['nombre'],
            'alertas': alcistas_item,
            'market_cap': item['market_cap']
        })
    if bajistas_item:
        alertas_bajistas.append({
            'accion': item['accion'],
            'nombre': item['nombre'],
            'alertas': bajistas_item,
            'market_cap': item['market_cap']
        })

# --- MOSTRAR ALERTAS ALCISTAS ---
if alertas_alcistas:
    st.markdown("""
    <div class="section-alcistas">
        <div class="section-title">📈 ALERTAS ALCISTAS</div>
    </div>
    """, unsafe_allow_html=True)
    
    for item in alertas_alcistas:
        accion = item['accion']
        nombre = item['nombre']
        alertas = item['alertas']
        market_cap = item['market_cap']
        market_cap_str = formatear_market_cap(market_cap) if market_cap > 0 else ""
        
        st.markdown(f"""
        <div class="alerta-card">
            <span class="icono-alcista">🟢</span>
            <span class="ticker">{accion}</span>
            <span class="empresa">{nombre}</span>
            <span class="mensaje">{alertas[0]}</span>
            <span class="marketcap">{market_cap_str}</span>
        </div>
        """, unsafe_allow_html=True)
        
        for alerta in alertas[1:]:
            st.markdown(f"""
            <div class="alerta-card" style="margin-left: 40px; border-left: 3px solid #16a34a;">
                <span class="icono-alcista">🟢</span>
                <span class="mensaje">{alerta}</span>
            </div>
            """, unsafe_allow_html=True)

# --- MOSTRAR ALERTAS BAJISTAS ---
if alertas_bajistas:
    st.markdown("""
    <div class="section-bajistas">
        <div class="section-title">📉 ALERTAS BAJISTAS</div>
    </div>
    """, unsafe_allow_html=True)
    
    for item in alertas_bajistas:
        accion = item['accion']
        nombre = item['nombre']
        alertas = item['alertas']
        market_cap = item['market_cap']
        market_cap_str = formatear_market_cap(market_cap) if market_cap > 0 else ""
        
        st.markdown(f"""
        <div class="alerta-card">
            <span class="icono-bajista">🔴</span>
            <span class="ticker">{accion}</span>
            <span class="empresa">{nombre}</span>
            <span class="mensaje">{alertas[0]}</span>
            <span class="marketcap">{market_cap_str}</span>
        </div>
        """, unsafe_allow_html=True)
        
        for alerta in alertas[1:]:
            st.markdown(f"""
            <div class="alerta-card" style="margin-left: 40px; border-left: 3px solid #dc2626;">
                <span class="icono-bajista">🔴</span>
                <span class="mensaje">{alerta}</span>
            </div>
            """, unsafe_allow_html=True)

# --- SI NO HAY ALERTAS ---
if not alertas_alcistas and not alertas_bajistas:
    st.info("✅ No hay alertas activas en este momento. Todas las acciones están en estado neutral.")

# --- FOOTER ---
st.markdown("""
<div class="footer">
    <p><strong>Señales de Trading</strong> · Datos en tiempo real vía Yahoo Finance · Análisis técnico automatizado</p>
    <p class="disclaimer">La información es orientativa y no constituye asesoramiento financiero. Las alertas se actualizan automáticamente cada 60 minutos.</p>
</div>
""", unsafe_allow_html=True)
