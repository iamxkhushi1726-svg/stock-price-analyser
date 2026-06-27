import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import (
    fetch_stock_data,
    get_stock_meta,
    POPULAR_STOCKS,
    PERIODS,
)
from src.indicators import add_all_indicators
from src.forecaster import forecast_next_days
from src.charts import (
    candlestick_chart,
    rsi_chart,
    volume_chart,
    forecast_chart,
)

# ── Page config ────────────────────────────────────────────────
st.set_page_config(
    page_title="Ticker · Stock Analyser",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Lora:ital,wght@0,400..700;1,400..700&family=Roboto:ital,wght@0,300;0,400;0,500;0,700;1,300&display=swap');

/* ── Reset & Base ──────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Roboto', sans-serif;
    background-color: #000000;
    color: #E5E5E5;
}

.stApp {
    background: #000000;
}

/* ── Sidebar ───────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #0A0A0A !important;
    border-right: 1px solid #1F1F1F;
}

[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label {
    color: #8C8C8C !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-family: 'Roboto', sans-serif !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label span {
    color: #D9D9D9 !important;
    font-size: 13px !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    font-weight: 400 !important;
}

[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div,
[data-testid="stSidebar"] [data-testid="stTextInput"] input {
    background: #141414 !important;
    border: 1px solid #262626 !important;
    color: #E5E5E5 !important;
    border-radius: 4px !important;
    font-family: 'Roboto', sans-serif !important;
    font-size: 13px !important;
}

[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div:hover,
[data-testid="stSidebar"] [data-testid="stTextInput"] input:focus {
    border-color: #FFFFFF !important;
    box-shadow: 0 0 0 1px #FFFFFF22 !important;
}

/* Sidebar brand mark */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 4px 0 20px 0;
    border-bottom: 1px solid #1F1F1F;
    margin-bottom: 24px;
}

.sidebar-brand-icon {
    width: 32px;
    height: 32px;
    background: #FFFFFF;
    color: #000000;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    font-weight: 700;
    line-height: 1;
    flex-shrink: 0;
}

.sidebar-brand-text {
    font-family: 'Instrument Serif', serif !important;
    font-size: 24px !important;
    font-weight: 400 !important;
    color: #FFFFFF !important;
    line-height: 0.9;
}

.sidebar-brand-sub {
    font-family: 'Roboto', sans-serif !important;
    font-size: 9px !important;
    color: #8C8C8C !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase;
    margin-top: 2px;
}

/* ── Checkboxes ────────────────────────────────────────────── */
[data-testid="stSidebar"] .stCheckbox label span {
    color: #D9D9D9 !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
}

/* ── Main content ──────────────────────────────────────────── */
.block-container {
    padding: 2.5rem 3rem 2.5rem 3rem !important;
    max-width: 100% !important;
}

/* ── Ticker header ─────────────────────────────────────────── */
.ticker-header {
    display: flex;
    align-items: baseline;
    gap: 16px;
    margin-bottom: 4px;
}

.ticker-name {
    font-family: 'Instrument Serif', serif;
    font-size: 52px;
    font-weight: 400;
    color: #FFFFFF;
    line-height: 1;
}

.ticker-symbol {
    font-family: 'Roboto', sans-serif;
    font-size: 13px;
    font-weight: 700;
    color: #FFFFFF;
    background: #1F1F1F;
    border: 1px solid #333333;
    padding: 2px 8px;
    border-radius: 3px;
    letter-spacing: 0.05em;
}

.ticker-meta {
    font-family: 'Lora', serif;
    font-size: 14px;
    color: #8C8C8C;
    font-weight: 400;
    margin-bottom: 32px;
}

.ticker-meta span {
    color: #434343;
    margin: 0 8px;
}

/* ── KPI Cards ─────────────────────────────────────────────── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 16px;
    margin-bottom: 32px;
}

.kpi-card {
    background: #0A0A0A;
    border: 1px solid #1F1F1F;
    border-radius: 4px;
    padding: 18px 20px;
    position: relative;
    transition: border-color 0.2s;
}

.kpi-card:hover {
    border-color: #333333;
}

.kpi-label {
    font-family: 'Roboto', sans-serif;
    font-size: 10px;
    font-weight: 500;
    color: #8C8C8C;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 10px;
}

.kpi-value {
    font-family: 'Instrument Serif', serif;
    font-size: 32px;
    font-weight: 400;
    color: #FFFFFF;
    line-height: 1;
}

.kpi-delta-pos {
    font-family: 'Roboto', sans-serif;
    font-size: 11px;
    font-weight: 400;
    color: #00E676;
    margin-top: 6px;
    display: inline-flex;
    align-items: center;
    gap: 3px;
}

.kpi-delta-neg {
    font-family: 'Roboto', sans-serif;
    font-size: 11px;
    font-weight: 400;
    color: #FF1744;
    margin-top: 6px;
    display: inline-flex;
    align-items: center;
    gap: 3px;
}

/* ── Section headers ───────────────────────────────────────── */
.section-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 18px;
    margin-top: 36px;
}

.section-title {
    font-family: 'Lora', serif;
    font-size: 16px;
    font-weight: 500;
    color: #FFFFFF;
}

.section-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1F1F1F, transparent);
}

/* ── Forecast badge ────────────────────────────────────────── */
.forecast-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 2px;
    font-family: 'Roboto', sans-serif;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.08em;
    margin-bottom: 12px;
}

.forecast-badge-up {
    background: #00E67614;
    border: 1px solid #00E67633;
    color: #00E676;
}

.forecast-badge-down {
    background: #FF174414;
    border: 1px solid #FF174433;
    color: #FF1744;
}

.forecast-caption {
    font-family: 'Lora', serif;
    font-size: 12px;
    color: #595959;
    margin-bottom: 16px;
    font-style: italic;
}

/* ── Divider ───────────────────────────────────────────────── */
.styled-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1F1F1F 20%, #1F1F1F 80%, transparent);
    margin: 32px 0;
}

/* ── Raw data table ────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: #0A0A0A !important;
    border: 1px solid #1F1F1F !important;
    border-radius: 4px !important;
}

[data-testid="stExpander"] summary {
    font-family: 'Roboto', sans-serif !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    color: #8C8C8C !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #1F1F1F !important;
    border-radius: 4px !important;
    overflow: hidden !important;
}

/* ── Footer ────────────────────────────────────────────────── */
.app-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 0 8px 0;
    border-top: 1px solid #1F1F1F;
    margin-top: 48px;
}

.footer-left, .footer-right {
    font-family: 'Roboto', sans-serif;
    font-size: 10px;
    color: #434343;
    letter-spacing: 0.05em;
}

/* ── Error state ───────────────────────────────────────────── */
[data-testid="stAlert"] {
    background: #140505 !important;
    border: 1px solid #5C1D1D !important;
    border-radius: 4px !important;
    color: #FF4D4D !important;
}

/* ── Spinner ───────────────────────────────────────────────── */
[data-testid="stSpinner"] > div {
    border-top-color: #FFFFFF !important;
}

/* ── Plotly charts ─────────────────────────────────────────── */
.js-plotly-plot {
    border-radius: 4px;
    overflow: hidden;
}

/* ── Scrollbar ─────────────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #000000; }
::-webkit-scrollbar-thumb { background: #262626; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #434343; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">◈</div>
        <div>
            <div class="sidebar-brand-text">Ticker</div>
            <div class="sidebar-brand-sub">MARKET INTELLIGENCE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    mode = st.radio(
        "Stock Selection",
        ["Popular Stocks", "Custom Ticker"],
        label_visibility="visible",
    )

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    if mode == "Popular Stocks":
        stock_label = st.selectbox("Choose Stock", list(POPULAR_STOCKS.keys()))
        ticker = POPULAR_STOCKS[stock_label]
    else:
        ticker = st.text_input(
            "Ticker Symbol",
            value="AAPL",
            help="Examples: AAPL, TSLA, TCS.NS, RELIANCE.NS",
        ).upper().strip()

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    period_label = st.selectbox("Time Period", list(PERIODS.keys()), index=3)
    period = PERIODS[period_label]

    st.markdown("<div style='height:16px; border-top: 1px solid #1F1F1F; margin-top:8px'></div>", unsafe_allow_html=True)

    st.markdown("""<p style='font-family: Roboto; font-size:10px; color:#8C8C8C; text-transform:uppercase; letter-spacing:0.1em; font-weight:500; margin-bottom:10px;'>Overlays</p>""", unsafe_allow_html=True)
    show_sma = st.checkbox("Moving Averages (SMA)", value=True)
    show_bb = st.checkbox("Bollinger Bands", value=False)
    show_forecast = st.checkbox("30-Day Forecast", value=True)

# ── Load data ──────────────────────────────────────────────────
with st.spinner(f"Loading {ticker}..."):
    df, info = fetch_stock_data(ticker, period)

if df is None or df.empty:
    st.error(f"No data found for **{ticker}**. Verify the symbol and try again.")
    st.stop()

df = add_all_indicators(df)
meta = get_stock_meta(info) if info else {}

# ── Computed values ────────────────────────────────────────────
company_name  = meta.get("name", ticker)
current_price = df["Close"].iloc[-1]
prev_price    = df["Close"].iloc[-2]
price_change  = current_price - prev_price
price_pct     = (price_change / prev_price) * 100
is_positive   = price_pct >= 0

mktcap = meta.get("market_cap", 0)
mktcap_str = (
    f"${mktcap/1e12:.2f}T" if mktcap >= 1e12 else
    f"${mktcap/1e9:.1f}B"  if mktcap >= 1e9  else
    f"${mktcap/1e6:.1f}M"  if mktcap >= 1e6  else
    "—"
)
pe = meta.get("pe_ratio")
pe_str = f"{pe:.2f}" if pe else "—"
delta_class = "kpi-delta-pos" if is_positive else "kpi-delta-neg"
delta_arrow = "▲" if is_positive else "▼"

# ── Ticker header ──────────────────────────────────────────────
st.markdown(f"""
<div class="ticker-header">
    <div class="ticker-name">{company_name}</div>
    <div class="ticker-symbol">{ticker}</div>
</div>
<div class="ticker-meta">
    {meta.get('sector', 'Equities')}
    <span>·</span>
    {meta.get('currency', 'USD')}
    <span>·</span>
    {period_label}
    <span>·</span>
    {df.index[-1].strftime('%b %d, %Y') if hasattr(df.index[-1], 'strftime') else 'Live'}
</div>
""", unsafe_allow_html=True)

# ── KPI strip ──────────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-label">Last Price</div>
        <div class="kpi-value">${current_price:,.2f}</div>
        <div class="{delta_class}">{delta_arrow} {abs(price_pct):.2f}%</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Day Change</div>
        <div class="kpi-value" style="color: {'#00E676' if is_positive else '#FF1744'}">
            {'+' if is_positive else ''}{price_change:+.2f}
        </div>
        <div class="{delta_class}">{delta_arrow} vs prev close</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">52W High</div>
        <div class="kpi-value">${meta.get('52w_high', 0):,.2f}</div>
        <div style="font-family:'Roboto',sans-serif;font-size:11px;color:#595959;margin-top:6px;">Annual peak</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">52W Low</div>
        <div class="kpi-value">${meta.get('52w_low', 0):,.2f}</div>
        <div style="font-family:'Roboto',sans-serif;font-size:11px;color:#595959;margin-top:6px;">Annual floor</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Market Cap</div>
        <div class="kpi-value">{mktcap_str}</div>
        <div style="font-family:'Roboto',sans-serif;font-size:11px;color:#595959;margin-top:6px;">P/E {pe_str}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Price chart ────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <span class="section-title">Price Action</span>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

fig_candle = candlestick_chart(df, ticker, show_sma=show_sma, show_bb=show_bb)
fig_candle.update_layout(
    paper_bgcolor="#000000",
    plot_bgcolor="#000000",
    font=dict(family="Roboto", color="#8C8C8C"),
    xaxis=dict(gridcolor="#1F1F1F", showgrid=True, zeroline=False),
    yaxis=dict(gridcolor="#1F1F1F", showgrid=True, zeroline=False),
    margin=dict(t=24, b=24, l=12, r=12),
)
st.plotly_chart(fig_candle, use_container_width=True)

# ── RSI + Volume ───────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <span class="section-title">Indicators</span>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

col_rsi, col_vol = st.columns([1, 1], gap="medium")

def _dark_layout(fig):
    fig.update_layout(
        paper_bgcolor="#000000",
        plot_bgcolor="#000000",
        font=dict(family="Roboto", color="#8C8C8C"),
        xaxis=dict(gridcolor="#1F1F1F", showgrid=True, zeroline=False),
        yaxis=dict(gridcolor="#1F1F1F", showgrid=True, zeroline=False),
        margin=dict(t=24, b=24, l=12, r=12),
    )
    return fig

with col_rsi:
    st.plotly_chart(_dark_layout(rsi_chart(df, ticker)), use_container_width=True)
with col_vol:
    st.plotly_chart(_dark_layout(volume_chart(df, ticker)), use_container_width=True)

# ── Forecast ───────────────────────────────────────────────────
if show_forecast:
    st.markdown("""
    <div class="section-header">
        <span class="section-title">30-Day Forecast</span>
        <div class="section-line"></div>
    </div>
    """, unsafe_allow_html=True)

    forecast_df, slope = forecast_next_days(df, days=30)
    is_up = slope > 0

    if is_up:
        badge = '<div class="forecast-badge forecast-badge-up">▲ UPWARD TREND · LINEAR REGRESSION</div>'
    else:
        badge = '<div class="forecast-badge forecast-badge-down">▼ DOWNWARD TREND · LINEAR REGRESSION</div>'

    st.markdown(badge, unsafe_allow_html=True)
    st.markdown("""<p class="forecast-caption">Model trained on historical closing prices. For research use only — not investment advice.</p>""", unsafe_allow_html=True)

    fig_fc = forecast_chart(df, forecast_df, ticker)
    fig_fc.update_layout(
        paper_bgcolor="#000000",
        plot_bgcolor="#000000",
        font=dict(family="Roboto", color="#8C8C8C"),
        xaxis=dict(gridcolor="#1F1F1F", showgrid=True, zeroline=False),
        yaxis=dict(gridcolor="#1F1F1F", showgrid=True, zeroline=False),
        margin=dict(t=24, b=24, l=12, r=12),
    )
    st.plotly_chart(fig_fc, use_container_width=True)

# ── Raw data ───────────────────────────────────────────────────
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
required_cols = ["Open", "High", "Low", "Close", "Volume", "SMA_20", "SMA_50", "RSI"]
available_cols = [c for c in required_cols if c in df.columns]

with st.expander("Raw Data · Last 30 Sessions"):
    st.dataframe(df[available_cols].tail(30), use_container_width=True)

# ── Footer ─────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    <div class="footer-left">DATA · YAHOO FINANCE · REAL-TIME DELAYED</div>
    <div class="footer-right">Built by Khushi &nbsp;·&nbsp; Project 06/100</div>
</div>
""", unsafe_allow_html=True)