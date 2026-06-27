import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


THEME = "plotly_dark"


def candlestick_chart(df, ticker, show_sma=True, show_bb=False):
    """
    Candlestick chart with optional SMA and Bollinger Band overlays.
    """
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Price",
        increasing_line_color="#2ecc71",
        decreasing_line_color="#e74c3c",
    ))

    if show_sma and "SMA_20" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["SMA_20"],
            name="SMA 20", line=dict(color="#f39c12", width=1.5),
        ))
    if show_sma and "SMA_50" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["SMA_50"],
            name="SMA 50", line=dict(color="#3498db", width=1.5),
        ))
    if show_bb and "BB_Upper" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["BB_Upper"],
            name="BB Upper", line=dict(color="#9b59b6", width=1, dash="dash"),
        ))
        fig.add_trace(go.Scatter(
            x=df.index, y=df["BB_Lower"],
            name="BB Lower", line=dict(color="#9b59b6", width=1, dash="dash"),
            fill="tonexty", fillcolor="rgba(155,89,182,0.05)",
        ))

    fig.update_layout(
        title=f"{ticker} — Price Chart",
        template=THEME,
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
        title_font_size=16,
        margin=dict(t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    return fig


def rsi_chart(df, ticker):
    """RSI chart with overbought/oversold reference lines."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=df["RSI"],
        name="RSI", line=dict(color="#e67e22", width=2),
    ))
    fig.add_hline(y=70, line_dash="dash", line_color="#e74c3c",
                  annotation_text="Overbought (70)")
    fig.add_hline(y=30, line_dash="dash", line_color="#2ecc71",
                  annotation_text="Oversold (30)")
    fig.update_layout(
        title=f"{ticker} — RSI (14)",
        template=THEME,
        yaxis=dict(range=[0, 100]),
        title_font_size=16,
        margin=dict(t=50, b=20),
    )
    return fig


def volume_chart(df, ticker):
    """Volume bar chart with 20-day moving average overlay."""
    colors = ["#2ecc71" if c >= o else "#e74c3c"
              for c, o in zip(df["Close"], df["Open"])]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df.index, y=df["Volume"],
        name="Volume", marker_color=colors, opacity=0.7,
    ))
    if "Volume_MA" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["Volume_MA"],
            name="Vol MA 20", line=dict(color="#f39c12", width=1.5),
        ))
    fig.update_layout(
        title=f"{ticker} — Volume",
        template=THEME,
        title_font_size=16,
        margin=dict(t=50, b=20),
    )
    return fig


def forecast_chart(df, forecast_df, ticker):
    """Price history + 30-day forecast on a single chart."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=df["Close"],
        name="Historical Price",
        line=dict(color="#3498db", width=2),
    ))
    fig.add_trace(go.Scatter(
        x=forecast_df.index, y=forecast_df["Forecast"],
        name="30-Day Forecast",
        line=dict(color="#e74c3c", width=2, dash="dash"),
    ))
    fig.update_layout(
        title=f"{ticker} — 30-Day Price Forecast",
        template=THEME,
        hovermode="x unified",
        title_font_size=16,
        margin=dict(t=50, b=20),
    )
    return fig