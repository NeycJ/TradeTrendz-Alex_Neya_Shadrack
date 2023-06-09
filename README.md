# TradeTrendz-Alex_Neya_Shadrack
TradeTrendz Final Project - Technical Analysis

The thesis of our project is to create tools that will allow an investor to accurately implement a trading strategy using a trading algorithm we have developed, test it, and determine stocks that will potentially work well with our specific algorithm. 

This project consists of a trading algorithm, a stock selector implemented in Python using the yfinance library and technical analysis indicators from the talib library. In addition we have machine learning models that work to predict future price action using an XG Boost model and Randsom Forrest model. 

## Trading Algorithm

The trading algorithm uses historical stock price data to identify potential buying and selling opportunities based on a set of predefined conditions. It utilizes the following indicators:

- Bollinger Bands: to identify potential entry and exit points based on price volatility.
- RSI (Relative Strength Index): to determine overbought and oversold conditions.
- Keltner Channels: to establish price range boundaries.
- Money Flow Index (MFI): to assess buying and selling pressure.

### Running the Trading Algorithm

1. Make sure you have Python installed on your machine.
2. Install the required libraries by running the following command in your terminal: `pip install yfinance pandas numpy talib`.
3. Clone the repository or download the project files.
4. Open the `trading_algo.ipynb` file in a Jupyter Notebook or any Python IDE.
5. Adjust the parameters in the algorithm according to your preferences.
6. Run the code to execute the trading algorithm.
7. The algorithm will prompt you to enter a ticker symbol for the stock you want to analyze.
8. After the algorithm finishes, it will display the results, including the trade journal, final balance, profit, number of trades, win rate percentage, and profit percentage.

## Stock Selector

The stock selector is designed to evaluate a list of ticker symbols and provide recommendations based on the historical performance of each stock. It applies similar technical analysis indicators as the trading algorithm, including RSI, Bollinger Bands, Keltner Channels, and Money Flow Index.

### Running the Stock Selector

1. Follow steps 1 to 4 from the Trading Algorithm section to set up the environment.
2. Open the `stock_selector.ipynb` file in a Jupyter Notebook or any Python IDE.
3. Modify the `tickerSymbols` list to include the ticker symbols you want to evaluate.
4. Adjust the parameters and criteria in the algorithm according to your preferences.
5. Run the code to execute the stock selector.
6. The stock selector will analyze the historical data for each ticker symbol and provide a list of recommended stocks based on the win ratio.

## Contributing

Contributions to this project are welcome! If you have any ideas, improvements, or bug fixes, please submit a pull request. For major changes, please open an issue first to discuss the proposed changes.

## License

This project is licensed under the MIT License.
