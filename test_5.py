import numpy as np

import matplotlib.pyplot as plt
import pandas as pd


def calculate_ema_5(data, window=5):
    """
    Calculate the exponential moving average (EMA) for the given data.

    Parameters:
        data (pandas Series): Pandas Series containing the closing prices.
        window (int): Number of periods to consider for the EMA calculation.

    Returns:
        pandas Series: EMA values for the given data.
    """
    # Calculate smoothing factor (alpha)
    alpha = 2 / (window + 1)

    # Initialize EMA Series with NaN values
    ema = pd.Series(index=data.index, dtype=float)
    ema.iloc[:window-1] = np.nan

    # Calculate SMA for the first window periods
    sma = data.iloc[:window].mean()

    # Set the first EMA value as the SMA
    ema.iloc[window-1] = sma

    # Calculate EMA for subsequent periods
    for i in range(window, len(data)):
        ema.iloc[i] = data.iloc[i] * alpha + ema.iloc[i - 1] * (1 - alpha)
    return ema