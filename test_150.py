import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



def calculate_ema_150(data, window=150):
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


# Plotting
plt.figure(figsize=(10, 6))
plt.plot(closing_prices_series, label='Closing Prices', color='blue')
plt.plot(ema_150, label='EMA (150 days)', color='red')
plt.title('Intraday Closing Prices and Exponential Moving Average (EMA)')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()