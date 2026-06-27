import pandas as pd
import numpy as np


def add_moving_averages(df, windows=None):
    """
    Add Simple Moving Average (SMA) columns to the DataFrame.
    Default windows: 20-day and 50-day.
    """

    if windows is None:
        windows = [20, 50]
    df = df.copy()
    for w in windows:
        df[f"SMA_{w}"] = df["Close"].rolling(window=w).mean()
    return df

def add_rsi(df, period=14):
    """
    Add Relative Strength Index (RSI) column.
    RSI > 70 = overbought, RSI < 30 = oversold.
    """    
    df = df.copy()
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss.replace(0, 1e-10)
    df["RSI"] = 100 - (100 / (1 + rs))
    return df

def add_bollinger_bands(df, window=20, num_std=2):
    """
    Add Bollinger Bands: upper, middle (SMA), and lower bands.
    Used to identify volatility and potential reversal points.
    """
    df = df.copy()
    sma = df["Close"].rolling(window=window).mean()
    std = df["Close"].rolling(window=window).std()
    df["BB_Upper"] = sma + (std * num_std)
    df["BB_Middle"] = sma
    df["BB_Lower"] = sma - (std * num_std)
    return df


def add_volume_ma(df, window=20):
    """Add a 20-day moving average of trading volume."""
    df = df.copy()
    df["Volume_MA"] = df["Volume"].rolling(window=window).mean()
    return df

def add_all_indicators(df):
    """Apply all indicators in one call. Returns enriched DataFrame."""
    df = add_moving_averages(df, windows=[20, 50])
    df = add_rsi(df, period=14)
    df = add_bollinger_bands(df, window=20)
    df = add_volume_ma(df, window=20)
    return df
    




