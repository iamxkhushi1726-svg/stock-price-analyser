import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def forecast_next_days(df, days=30):
    """
    Forecast next N days of closing price using Linear Regression on a numeric time.
    Simple but explainable -  good for portfolio.
    Returns a DataFrame with future dates and predicted prices.
    """
    df_clean = df[["Close"]].dropna().copy()
    df_clean["day_num"] = np.arange(len(df_clean))

    X = df_clean[["day_num"]].values
    y = df_clean["Close"].values

    model = LinearRegression()
    model.fit(X, y)

    last_day = df_clean["day_num"].iloc[-1]
    future_days = np.arange(last_day + 1, last_day + days + 1).reshape(-1, 1)
    predicted_prices = model.predict(future_days)

    last_date = df_clean.index[-1]
    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=days,
        freq="B"
    )

    forecast_df = pd.DataFrame({
        "Date": future_dates,
        "Forecast": predicted_prices,
    }).set_index("Date")

    return forecast_df, model.coef_[0]