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
