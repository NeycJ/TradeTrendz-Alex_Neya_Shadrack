import yfinance as yf
import pandas as pd
import numpy as np
from talib import BBANDS, RSI, MA_Type, ATR, MFI
import datetime as dt

# Download historical data
tickerSymbol = input("What stock are we crushing today?: ")
# Get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
# Get the historical prices for this ticker
df = tickerData.history(period='60d', interval='5m')

# Calculate Bollinger Bands
df['upper_band'], df['middle_band'], df['lower_band'] = BBANDS(df['Close'], timeperiod=20)

# Calculate RSI
df['rsi'] = RSI(df['Close'], timeperiod=14)

# Calculate Keltner Channels
df['keltner_middle'] = df['Close'].rolling(window=20).mean()
df['atr'] = ATR(df['High'], df['Low'], df['Close'], timeperiod=20)
df['keltner_upper'] = df['keltner_middle'] + (df['atr'] * 1.5)
df['keltner_lower'] = df['keltner_middle'] - (df['atr'] * 1.5)

# Calculate Money Flow Index
df['mfi'] = MFI(df['High'], df['Low'], df['Close'], df['Volume'], timeperiod=14)

starting_balance = 50000
risk_amount = (.40 * starting_balance) # 40% of starting balance
stop_loss_pct = 0.15 # 15%
balance = starting_balance
position = 0
entry_price = 0
num_shares = 0

# Initialize trade journal
trade_journal = pd.DataFrame(columns=["Date", "Action", "Price", "Shares", "Balance"])

# Iterate over the data
for i, row in df.iterrows():
    # Check if RSI is below 20 and close price is below the lower Keltner Channel or lower Bollinger Band
    if row['rsi'] < 20 and (row['Close'] <  row['keltner_lower'] or row['Close'] < row['lower_band']):
        if position == 0:
            num_shares = int(risk_amount / row['Close'])
            balance -= num_shares * row['Close']
            position += num_shares
            entry_price = row['Close']
            trade_journal = trade_journal.append({"Date": row.name, "Action": "Buy", "Price": row["Close"], "Shares": num_shares, "Balance": balance}, ignore_index=True)
    elif ((row['rsi'] > 80 and (row['Close'] > row['keltner_upper'] or row['Close'] > row['upper_band'])) or 
          (entry_price > 0 and row['Close'] < entry_price * (1 - stop_loss_pct)) or 
          (row['mfi'] < 57 and row['rsi'] > 80)):
        if position > 0:
            balance += position * row['Close']
            trade_journal = trade_journal.append({"Date": row.name, "Action": "Sell", "Price": row["Close"], "Shares": position, "Balance": balance}, ignore_index=True)
            position = 0

# Separate dataframes for buy and sell operations
buy_df = trade_journal[trade_journal["Action"] == "Buy"].copy()
sell_df = trade_journal[trade_journal["Action"] == "Sell"].copy()



# Ensure that the number of 'Buy' transactions is equal to the number of 'Sell' transactions
# A single 'Buy' without a corresponding 'Sell' is not counted as a complete trade
if len(buy_df) != len(sell_df):
    if len(buy_df) > len(sell_df):
        buy_df = buy_df.iloc[:-1, :]  # Remove the last 'Buy' operation
    else:
        sell_df = sell_df.iloc[:-1, :]  # Remove the last 'Sell' operation

# Compute the number of completed trades
num_of_trades = len(buy_df)

# Reset indices of buy_df and sell_df
buy_df.reset_index(drop=True, inplace=True)
sell_df.reset_index(drop=True, inplace=True)

# Compute Win/Loss ratio
sell_df["Win"] = sell_df["Price"] > buy_df["Price"]
win_loss_ratio = sell_df["Win"].sum() / num_of_trades

# Compute ROI
sell_df["ROI"] = (sell_df["Price"] - buy_df["Price"]) / buy_df["Price"]
average_roi = sell_df["ROI"].mean()

# Aggregate the results
result = {"Ticker": tickerSymbol,
          "Average ROI": average_roi * 100}

final_df = pd.DataFrame(result, index=[0])


# Compute the win ratio and the total profit
win_ratio = sell_df["Win"].sum() / num_of_trades
total_profit = balance - starting_balance

# Compute profit percentage
profit_percentage = (total_profit / starting_balance) * 100


print(final_df)
print(f"Trade Journal:\n{trade_journal}")
print(f"Final Balance: ${balance:.2f}")
print(f"Profit: ${total_profit:.2f}")
print(f"Number of Trades: {num_of_trades}")
print(f"Win Rate Percentage: {win_ratio * 100:.2f}%")
print("Profit Percentage: ", profit_percentage, "%")

# Print statements based on profit percentage
if trade_journal.iloc[-1]['Action'] == 'Buy':
    print("Looks bad, but you still have a position open.")
elif profit_percentage > 2:
    print("Looks like we're crushin' it..$$$")
elif 0 <= profit_percentage <= 1:
    print("Could be better..")
else:
    print("Ouch.. back to the drawing board for this one..")