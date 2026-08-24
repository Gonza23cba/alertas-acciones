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
    page_title="RSI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# LISTA DE ACCIONES (ACTUALIZAR AQUÍ)
# ============================================



LISTA_ACCIONES = [
    "BKR", "CVX", "HAL", "OXY", "PSX", "SLB", "URA", "VST", "XOM",
    "AAPL", "ADBE", "ADI", "AI", "ALAB", "AMAT", "AMD", "ASTS", "AVGO",
    "CRM", "CRWD", "CRWV", "CSCO", "FSLR", "GLW", "IBM", "INTC", "LRCX",
    "MRVL", "MSFT", "MSI", "MSTR", "MU", "NOW", "NVDA", "ONDS", "ORCL",
    "PANW", "PATH", "PLTR", "QCOM", "RGTI", "SNDK", "SNOW", "SPCX",
    "TEAM", "TXN", "UBER", "VRSN", "XYZ", "SKHY",
    "AIG", "AXP", "BAC", "KEEL", "BK", "BRK.B", "C", "COIN", "GS",
    "HOOD", "HUT", "JPM", "MA", "MRSH", "PYPL", "RIOT", "SCHW", "SPGI",
    "TRV", "USB", "V", "WFC",
    "DIS", "GOOGL", "META", "NFLX", "RBLX", "ROKU", "T", "TWLO", "VZ", "ZM",
    "BG", "CL", "COST", "HSY", "KMB", "KO", "MDLZ", "MO", "PEP", "PG",
    "SYY", "TGT", "WMT",
    "CEG", "OKLO", "VST",
    "AAL", "ADP", "AVY", "BA", "CAT", "DAL", "DE", "FDX", "GE",
    "HON", "HWM", "LMT", "MMM", "PCAR", "RKLB", "RTX", "SNA", "UAL", "UNP",
    "ABBV", "ABT", "AMGN", "BMY", "CAH", "CVS", "DHR", "GILD", "ISRG",
    "JNJ", "LLY", "MDT", "MRK", "MRNA", "PFE", "TEM", "TMO", "UNH", "VRTX",
    "BABA", "BIDU", "JD", "NIO", "NTES", "PDD", "XPEV",
    "AMX", "ASR", "CX", "FMX", "KOF", "PAC",
    "GFI", "HMY", "JMIA", "AEM", "B", "BB", "CLS", "LAC", "MUX", "NG", "NXE", "PAAS",
    "SHOP", "ABEV", "BAK", "BBD", "EMBJ", "GGB", "ITUB", "LND", "NU", "PAGS",
    "PBR", "SID", "SUZ", "UGP", "VALE", "XP",
    "ARM", "AZN", "BCS", "BP", "DEO", "GSK", "HSBC", "LYG", "NGG", "RIO", "UL", "VOD",
    "ACN", "AEG", "ASML", "BBVA", "E", "EQNR", "GRMN", "ING", "NBIS", "NVS",
    "PHG", "RACE", "SAN", "SAP", "SHEL", "SPOT", "STLA", "TEF", "TMUS",
    "TS", "TTE", "TX", "BHP", "HDB", "HMC", "IBN", "INFY", "IREN", "KB",
    "PKX", "SE", "SONY", "TM", "TSM",
    "ALUA", "BBAR", "BMA", "BYMA", "CEPU", "COME", "CRESY", "EDN",
    "GGAL", "GLOB", "HARG", "LOMA", "MELI", "MIRG", "PAMP", "SUPV",
    "TECO2", "TGNO4", "TGSU2", "TRAN", "TXAR", "VALO", "VIST", "YPFD"
    # Agrega más acciones aquí
]

NOMBRES_EMPRESAS = {
    # Energy
    "BKR": "Baker Hughes Co.",
    "CVX": "Chevron Corp.",
    "HAL": "Halliburton Co.",
    "OXY": "Occidental Petroleum Corp.",
    "PSX": "Phillips 66",
    "SLB": "Schlumberger Ltd.",
    "URA": "Uranium Energy Corp.",
    "VST": "Vistra Corp.",
    "XOM": "Exxon Mobil Corp.",
    # Technology
    "AAPL": "Apple Inc.",
    "ADBE": "Adobe Inc.",
    "ADI": "Analog Devices Inc.",
    "AI": "C3.ai Inc.",
    "ALAB": "Astera Labs Inc.",
    "AMAT": "Applied Materials Inc.",
    "AMD": "Advanced Micro Devices Inc.",
    "ASTS": "AST SpaceMobile Inc.",
    "AVGO": "Broadcom Inc.",
    "CRM": "Salesforce Inc.",
    "CRWD": "CrowdStrike Holdings Inc.",
    "CRWV": "CoreWeave Inc.",
    "CSCO": "Cisco Systems Inc.",
    "FSLR": "First Solar Inc.",
    "GLW": "Corning Inc.",
    "IBM": "International Business Machines Corp.",
    "INTC": "Intel Corp.",
    "LRCX": "Lam Research Corp.",
    "MRVL": "Marvell Technology Inc.",
    "MSFT": "Microsoft Corp.",
    "MSI": "Motorola Solutions Inc.",
    "MSTR": "MicroStrategy Inc.",
    "MU": "Micron Technology Inc.",
    "NOW": "ServiceNow Inc.",
    "NVDA": "NVIDIA Corp.",
    "ONDS": "Ondas Holdings Inc.",
    "ORCL": "Oracle Corp.",
    "PANW": "Palo Alto Networks Inc.",
    "PATH": "UiPath Inc.",
    "PLTR": "Palantir Technologies Inc.",
    "QCOM": "Qualcomm Inc.",
    "RGTI": "Rigetti Computing Inc.",
    "SNDK": "Sandisk Corp.",
    "SNOW": "Snowflake Inc.",
    "SPCX": "SpacX Corp.",
    "TEAM": "Atlassian Corp.",
    "TXN": "Texas Instruments Inc.",
    "UBER": "Uber Technologies Inc.",
    "VRSN": "Verisign Inc.",
    "XYZ": "Block Inc.",
    "SKHY": "SK Hynix Inc.",
    # Financial
    "AIG": "American International Group Inc.",
    "AXP": "American Express Co.",
    "BAC": "Bank of America Corp.",
    "KEEL": "Keel Holdings Inc.",
    "BK": "Bank of New York Mellon Corp.",
    "BRK.B": "Berkshire Hathaway Inc.",
    "C": "Citigroup Inc.",
    "COIN": "Coinbase Global Inc.",
    "GS": "Goldman Sachs Group Inc.",
    "HOOD": "Robinhood Markets Inc.",
    "HUT": "Hut 8 Mining Corp.",
    "JPM": "JPMorgan Chase & Co.",
    "MA": "Mastercard Inc.",
    "MRSH": "Marsh & McLennan Companies Inc.",
    "PYPL": "PayPal Holdings Inc.",
    "RIOT": "Riot Platforms Inc.",
    "SCHW": "Charles Schwab Corp.",
    "SPGI": "S&P Global Inc.",
    "TRV": "The Travelers Companies Inc.",
    "USB": "U.S. Bancorp",
    "V": "Visa Inc.",
    "WFC": "Wells Fargo & Co.",
    # Communication Services
    "DIS": "Walt Disney Co.",
    "GOOGL": "Alphabet Inc.",
    "META": "Meta Platforms Inc.",
    "NFLX": "Netflix Inc.",
    "RBLX": "Roblox Corp.",
    "ROKU": "Roku Inc.",
    "T": "AT&T Inc.",
    "TWLO": "Twilio Inc.",
    "VZ": "Verizon Communications Inc.",
    "ZM": "Zoom Video Communications Inc.",
    # Consumer Cyclical
    "BG": "Bunge Global SA",
    "CL": "Colgate-Palmolive Co.",
    "COST": "Costco Wholesale Corp.",
    "HSY": "The Hershey Co.",
    "KMB": "Kimberly-Clark Corp.",
    "KO": "The Coca-Cola Co.",
    "MDLZ": "Mondelez International Inc.",
    "MO": "Altria Group Inc.",
    "PEP": "PepsiCo Inc.",
    "PG": "Procter & Gamble Co.",
    "SYY": "Sysco Corp.",
    "TGT": "Target Corp.",
    "WMT": "Walmart Inc.",
    # Utilities
    "CEG": "Constellation Energy Corp.",
    "OKLO": "Oklo Inc.",
    # Industrials
    "AAL": "American Airlines Group Inc.",
    "ADP": "Automatic Data Processing Inc.",
    "AVY": "Avery Dennison Corp.",
    "BA": "Boeing Co.",
    "CAT": "Caterpillar Inc.",
    "DAL": "Delta Air Lines Inc.",
    "DE": "Deere & Co.",
    "FDX": "FedEx Corp.",
    "GE": "General Electric Co.",
    "HON": "Honeywell International Inc.",
    "HWM": "Howmet Aerospace Inc.",
    "LMT": "Lockheed Martin Corp.",
    "MMM": "3M Co.",
    "PCAR": "PACCAR Inc.",
    "RKLB": "Rocket Lab USA Inc.",
    "RTX": "RTX Corp.",
    "SNA": "Snap-on Inc.",
    "UAL": "United Airlines Holdings Inc.",
    "UNP": "Union Pacific Corp.",
    # HealthCare
    "ABBV": "AbbVie Inc.",
    "ABT": "Abbott Laboratories",
    "AMGN": "Amgen Inc.",
    "BMY": "Bristol-Myers Squibb Co.",
    "CAH": "Cardinal Health Inc.",
    "CVS": "CVS Health Corp.",
    "DHR": "Danaher Corp.",
    "GILD": "Gilead Sciences Inc.",
    "ISRG": "Intuitive Surgical Inc.",
    "JNJ": "Johnson & Johnson",
    "LLY": "Eli Lilly and Co.",
    "MDT": "Medtronic PLC",
    "MRK": "Merck & Co. Inc.",
    "MRNA": "Moderna Inc.",
    "PFE": "Pfizer Inc.",
    "TEM": "Tempus AI Inc.",
    "TMO": "Thermo Fisher Scientific Inc.",
    "UNH": "UnitedHealth Group Inc.",
    "VRTX": "Vertex Pharmaceuticals Inc.",
    # Emerging Markets
    "BABA": "Alibaba Group Holding Ltd.",
    "BIDU": "Baidu Inc.",
    "JD": "JD.com Inc.",
    "NIO": "NIO Inc.",
    "NTES": "NetEase Inc.",
    "PDD": "PDD Holdings Inc.",
    "XPEV": "XPeng Inc.",
    "AMX": "América Móvil S.A.B. de C.V.",
    "ASR": "Grupo Aeroportuario del Sureste S.A.B. de C.V.",
    "CX": "Cemex S.A.B. de C.V.",
    "FMX": "Fomento Económico Mexicano S.A.B. de C.V.",
    "KOF": "Coca-Cola FEMSA S.A.B. de C.V.",
    "PAC": "Grupo Aeroportuario del Pacífico S.A.B. de C.V.",
    "NU": "Nu Holdings Ltd.",
    "PAGS": "PagSeguro Digital Ltd.",
    "XP": "XP Inc.",
    "ABEV": "Ambev S.A.",
    "BAK": "Braskem S.A.",
    "BBD": "Banco Bradesco S.A.",
    "EMBJ": "Embraer S.A.",
    "GGB": "Gerdau S.A.",
    "ITUB": "Itaú Unibanco Holding S.A.",
    "LND": "BrasilAgro - Companhia Brasileira de Propriedades Agrícolas",
    "PBR": "Petrobras",
    "SID": "Companhia Siderúrgica Nacional",
    "SUZ": "Suzano Papel e Celulose S.A.",
    "UGP": "Ultrapar Participações S.A.",
    "VALE": "Vale S.A.",
    # European
    "ARM": "Arm Holdings PLC",
    "AZN": "AstraZeneca PLC",
    "BCS": "Barclays PLC",
    "BP": "BP PLC",
    "DEO": "Diageo PLC",
    "GSK": "GSK PLC",
    "HSBC": "HSBC Holdings PLC",
    "LYG": "Lloyds Banking Group PLC",
    "NGG": "National Grid PLC",
    "RIO": "Rio Tinto Group",
    "UL": "Unilever PLC",
    "VOD": "Vodafone Group PLC",
    "AEG": "Aegon Ltd.",
    "ASML": "ASML Holding N.V.",
    "BBVA": "Banco Bilbao Vizcaya Argentaria S.A.",
    "E": "Eni S.p.A.",
    "EQNR": "Equinor ASA",
    "GRMN": "Garmin Ltd.",
    "ING": "ING Groep N.V.",
    "NBIS": "Nebius Group N.V.",
    "NVS": "Novartis AG",
    "PHG": "Koninklijke Philips N.V.",
    "RACE": "Ferrari N.V.",
    "SAN": "Banco Santander S.A.",
    "SAP": "SAP SE",
    "SHEL": "Shell PLC",
    "SPOT": "Spotify Technology S.A.",
    "STLA": "Stellantis N.V.",
    "TEF": "Telefónica S.A.",
    "TMUS": "T-Mobile US Inc.",
    "TS": "Tenaris S.A.",
    "TTE": "TotalEnergies SE",
    "TX": "Ternium S.A.",
    # Japan & Asia
    "HMC": "Honda Motor Co. Ltd.",
    "SONY": "Sony Group Corp.",
    "TM": "Toyota Motor Corp.",
    "TSM": "Taiwan Semiconductor Manufacturing Co. Ltd.",
    "BHP": "BHP Group Ltd.",
    "HDB": "HDFC Bank Ltd.",
    "IBN": "ICICI Bank Ltd.",
    "INFY": "Infosys Ltd.",
    "IREN": "Iren S.p.A.",
    "KB": "KB Financial Group Inc.",
    "PKX": "POSCO Holdings Inc.",
    "SE": "Sea Ltd.",
    "SHOP": "Shopify Inc.",
    "ACN": "Accenture PLC",
    # Argentina
    "ALUA": "Aluar Aluminio Argentino S.A.I.C.",
    "BBAR": "Banco BBVA Argentina S.A.",
    "BMA": "Banco Macro S.A.",
    "BYMA": "Bolsas y Mercados Argentinos S.A.",
    "CEPU": "Central Puerto S.A.",
    "COME": "Comercial del Plata S.A.",
    "CRESY": "Cresud S.A.C.I.F. y A.",
    "EDN": "Edenor S.A.",
    "GGAL": "Grupo Financiero Galicia S.A.",
    "GLOB": "Globant S.A.",
    "HARG": "Holcim Argentina S.A.",
    "LOMA": "Loma Negra C.I.A.S.A.",
    "MELI": "MercadoLibre Inc.",
    "MIRG": "Mirgor S.A.",
    "PAMP": "Pampa Energía S.A.",
    "SUPV": "Grupo Supervielle S.A.",
    "TECO2": "Telecom Argentina S.A.",
    "TGNO4": "Ternium Argentina S.A.",
    "TGSU2": "Transener S.A.",
    "TRAN": "Transportadora de Gas del Sur S.A.",
    "TXAR": "Ternium S.A.",
    "VALO": "Valor S.A.",
    "VIST": "Vista Energy S.A.B. de C.V.",
    "YPFD": "YPF S.A.",
    # Mining & Metals
    "AEM": "Agnico Eagle Mines Ltd.",
    "GFI": "Gold Fields Ltd.",
    "HMY": "Harmony Gold Mining Company Ltd.",
    "JMIA": "Jumia Technologies AG",
    "LAC": "Lithium Americas Corp.",
    "MUX": "McEwen Mining Inc.",
    "NG": "NovaGold Resources Inc.",
    "NXE": "NexGen Energy Ltd.",
    "PAAS": "Pan American Silver Corp.",
    # Others / Additional
    "B": "Barnes Group Inc.",
    "BB": "BlackBerry Ltd.",
    "CLS": "Celestica Inc.",
}


def get_nombre_empresa(simbolo):
    return NOMBRES_EMPRESAS.get(simbolo, simbolo)

# ============================================
# PARÁMETROS
# ============================================

INTERVALO_SEGUNDOS = 1800  # 30 minutos

# ============================================
# FUNCIONES
# ============================================

@st.cache_data(ttl=1800)
def obtener_datos(simbolo, dias=90):
    try:
        ticker = yf.Ticker(simbolo)
        df = ticker.history(period=f"{dias}d")
        if df.empty:
            return None
        return df
    except:
        return None

def calcular_rsi(df):
    try:
        rsi = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
        return round(rsi.iloc[-1], 2)
    except:
        return None

def get_rsi_status(rsi):
    if rsi is None:
        return "Sin datos", "#6c757d", "⚪"
    elif rsi > 70:
        return "SOBRECOMPRA", "#8b1a1a", "🔴"
    elif rsi >= 65:
        return "Próxima a SOBRECOMPRA", "#a0522d", "🟠"
    elif rsi < 30:
        return "SOBREVENTA", "#16a34a", "🟢"
    elif rsi <= 35:
        return "Próxima a SOBREVENTA", "#003A8C", "🔵"
    else:
        return "Neutral", "#6c757d", "⚪"

# ============================================
# INTERFAZ PRINCIPAL (SIN ENCABEZADO)
# ============================================

# --- INICIALIZAR SESSION STATE ---
if 'resultados' not in st.session_state:
    st.session_state.resultados = []
if 'ultima_actualizacion' not in st.session_state:
    st.session_state.ultima_actualizacion = None

# --- EJECUCIÓN AUTOMÁTICA ---
if (st.session_state.ultima_actualizacion is None or 
    (datetime.now() - st.session_state.ultima_actualizacion).total_seconds() > INTERVALO_SEGUNDOS):
    with st.spinner("Calculando RSI..."):
        st.session_state.resultados = []
        for accion in LISTA_ACCIONES:
            df = obtener_datos(accion)
            if df is not None and not df.empty:
                rsi = calcular_rsi(df)
                estado, color, emoji = get_rsi_status(rsi)
                st.session_state.resultados.append({
                    'Acción': accion,
                    'Empresa': get_nombre_empresa(accion),
                    'RSI': rsi,
                    'Estado': estado,
                    'Emoji': emoji,
                    'Color': color
                })
            else:
                st.session_state.resultados.append({
                    'Acción': accion,
                    'Empresa': get_nombre_empresa(accion),
                    'RSI': None,
                    'Estado': 'Sin datos',
                    'Emoji': '❌',
                    'Color': '#6c757d'
                })
        st.session_state.ultima_actualizacion = datetime.now()
    st.rerun()

# --- MOSTRAR ESTADÍSTICAS ---
if st.session_state.resultados:
    total = len(st.session_state.resultados)
    sobreventa = sum(1 for r in st.session_state.resultados if r['Estado'] == 'SOBREVENTA')
    prox_sobreventa = sum(1 for r in st.session_state.resultados if r['Estado'] == 'Próxima a SOBREVENTA')
    sobrecompra = sum(1 for r in st.session_state.resultados if r['Estado'] == 'SOBRECOMPRA')
    prox_sobrecompra = sum(1 for r in st.session_state.resultados if r['Estado'] == 'Próxima a SOBRECOMPRA')
    neutral = sum(1 for r in st.session_state.resultados if r['Estado'] == 'Neutral')
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("📊 Total", total)
    with col2:
        st.metric("🟢 Sobreventa", sobreventa, delta_color="normal")
    with col3:
        st.metric("🔵 Próx. Sobreventa", prox_sobreventa, delta_color="normal")
    with col4:
        st.metric("🔴 Sobrecompra", sobrecompra, delta_color="inverse")
    with col5:
        st.metric("🟠 Próx. Sobrecompra", prox_sobrecompra, delta_color="inverse")
    with col6:
        st.metric("⚪ Neutral", neutral)
    
    st.caption(f"🔄 Última actualización: {st.session_state.ultima_actualizacion.strftime('%d/%m/%Y %H:%M:%S')}")
    st.markdown("---")

    # ============================================
    # ORGANIZACIÓN EN DOS COLUMNAS
    # ============================================
    
    # Separar acciones por estado
    acciones_sobreventa = [r for r in st.session_state.resultados if r['Estado'] == 'SOBREVENTA']
    acciones_prox_sobreventa = [r for r in st.session_state.resultados if r['Estado'] == 'Próxima a SOBREVENTA']
    acciones_sobrecompra = [r for r in st.session_state.resultados if r['Estado'] == 'SOBRECOMPRA']
    acciones_prox_sobrecompra = [r for r in st.session_state.resultados if r['Estado'] == 'Próxima a SOBRECOMPRA']
    acciones_neutral = [r for r in st.session_state.resultados if r['Estado'] == 'Neutral']
    
    # Crear columnas
    col_izquierda, col_derecha = st.columns(2)
    
    # ============================================
    # COLUMNA IZQUIERDA: SOBREVENTA + PRÓXIMA SOBREVENTA
    # ============================================
    with col_izquierda:
        st.markdown("### 🟢 Zona de Sobreventa")
        
        if acciones_sobreventa:
            for r in acciones_sobreventa:
                st.markdown(f"""
                <div style="background:#f0fdf4; border:2px solid #16a34a; border-radius:8px; padding:10px 14px; margin-bottom:8px;">
                    <strong>{r['Acción']}</strong> · {r['Empresa']} · 
                    <span style="color:#16a34a; font-weight:700;">RSI: {r['RSI']}</span> · 
                    <span style="color:#16a34a;">{r['Emoji']} {r['Estado']}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No hay acciones en sobreventa")
        
        st.markdown("---")
        st.markdown("### 🔵 Próxima a Sobreventa (30-35)")
        
        if acciones_prox_sobreventa:
            for r in acciones_prox_sobreventa:
                st.markdown(f"""
                <div style="background:#e8f0fe; border:2px solid #003A8C; border-radius:8px; padding:10px 14px; margin-bottom:8px;">
                    <strong>{r['Acción']}</strong> · {r['Empresa']} · 
                    <span style="color:#003A8C; font-weight:700;">RSI: {r['RSI']}</span> · 
                    <span style="color:#003A8C;">{r['Emoji']} {r['Estado']}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No hay acciones próximas a sobreventa")
    
    # ============================================
    # COLUMNA DERECHA: SOBRECOMPRA + PRÓXIMA SOBRECOMPRA
    # ============================================
    with col_derecha:
        st.markdown("### 🔴 Zona de Sobrecompra")
        
        if acciones_sobrecompra:
            for r in acciones_sobrecompra:
                st.markdown(f"""
                <div style="background:#fef2f2; border:2px solid #8b1a1a; border-radius:8px; padding:10px 14px; margin-bottom:8px;">
                    <strong>{r['Acción']}</strong> · {r['Empresa']} · 
                    <span style="color:#8b1a1a; font-weight:700;">RSI: {r['RSI']}</span> · 
                    <span style="color:#8b1a1a;">{r['Emoji']} {r['Estado']}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No hay acciones en sobrecompra")
        
        st.markdown("---")
        st.markdown("### 🟠 Próxima a Sobrecompra (65-70)")
        
        if acciones_prox_sobrecompra:
            for r in acciones_prox_sobrecompra:
                st.markdown(f"""
                <div style="background:#fff7ed; border:2px solid #a0522d; border-radius:8px; padding:10px 14px; margin-bottom:8px;">
                    <strong>{r['Acción']}</strong> · {r['Empresa']} · 
                    <span style="color:#a0522d; font-weight:700;">RSI: {r['RSI']}</span> · 
                    <span style="color:#a0522d;">{r['Emoji']} {r['Estado']}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No hay acciones próximas a sobrecompra")
    
    # ============================================
    # ACCIONES NEUTRALES (repartidas abajo)
    # ============================================
    if acciones_neutral:
        st.markdown("---")
        st.markdown("### ⚪ Acciones Neutrales")
        
        # Repartir neutrales en dos columnas
        mitad = len(acciones_neutral) // 2
        col_n1, col_n2 = st.columns(2)
        
        with col_n1:
            for r in acciones_neutral[:mitad]:
                st.markdown(f"""
                <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:8px 14px; margin-bottom:6px;">
                    <strong>{r['Acción']}</strong> · {r['Empresa']} · 
                    <span style="color:#6c757d; font-weight:500;">RSI: {r['RSI']}</span> · 
                    <span style="color:#6c757d;">⚪ Neutral</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col_n2:
            for r in acciones_neutral[mitad:]:
                st.markdown(f"""
                <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:8px 14px; margin-bottom:6px;">
                    <strong>{r['Acción']}</strong> · {r['Empresa']} · 
                    <span style="color:#6c757d; font-weight:500;">RSI: {r['RSI']}</span> · 
                    <span style="color:#6c757d;">⚪ Neutral</span>
                </div>
                """, unsafe_allow_html=True)