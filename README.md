# Stock-Correlation-Analysis
Example Stock Correlation Analysis script to calculate a stock's correlation to its respective market index over a specific time period.

Very basic script but the idea is that you can use it to enter a ticker and market index for a specific time period (by updating the start_date and end_date variable) to pull the daily returns for the stock and market index. The correlation is then calculated using Pearson Correlation coefficient. The daily price returns are downloaded using yahoo finance.

Instructions for Use:

1.  **Dependencies**: Ensure you have `yfinance`, `pandas`, `matplotlib`,
    and `seaborn` installed (`pip install yfinance pandas matplotlib seaborn`).
2.  **Input Variables**:
    *   `stock_tickers`: A list of stock symbols you wish to analyze.
    *   `market_index_tickers`: A list of market index symbols.
    *   `start_date` and `end_date`: Define the period for data analysis.
    *   `stock_to_market_map`: **Crucially, define this dictionary to map
        each stock ticker to its respective market index ticker.**
        If you change `stock_tickers` or `market_index_tickers`, you MUST
        update this mapping accordingly.
3.  **Execution**: Run the entire script. It will download data, perform
    calculations, print the correlations, and display a bar chart.

Example Configuration:

Below are the default input variables, which can be modified by the user.

--- 1. Import necessary libraries ---
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

 --- 2. Define user input variables ---
# List of stock tickers to analyze
stock_tickers = ['VOD', 'BP.L', 'NVDA', 'AAPL', 'RHM.DE', 'SAP.DE', 'OR.PA', 'MC.PA']
# List of market index tickers corresponding to the stocks
market_index_tickers = ['^FTSE', '^GDAXI', '^FCHI', '^GSPC']
# Define the start and end dates for data download
start_date = '2025-01-01'
end_date = '2025-12-31'

# Define the mapping between each stock and its corresponding market index.
# This dictionary is crucial for pairing stocks with their relevant market.
stock_to_market_map = {
    'VOD': '^FTSE',    # Vodafone (UK) mapped to FTSE 100
    'BP.L': '^FTSE',   # BP (UK) mapped to FTSE 100
    'NVDA': '^GSPC',   # NVIDIA (US) mapped to S&P 500
    'AAPL': '^GSPC',   # Apple (US) mapped to S&P 500
    'RHM.DE': '^GDAXI',# Rheinmetall (Germany) mapped to DAX
    'SAP.DE': '^GDAXI',# SAP (Germany) mapped to DAX
    'OR.PA': '^FCHI',  # Orange (France) mapped to CAC 40
    'MC.PA': '^FCHI'   # LVMH (France) mapped to CAC 40
}

--- 3. Implement Data Download and Preprocessing ---

print(f"Downloading stock data for {stock_tickers} from {start_date} to {end_date}...")
# Download historical stock data using yfinance
# 'auto_adjust=True' ensures that adjusted close prices are used,
# and 'actions=False' prevents downloading dividend/split information
stock_data = yf.download(stock_tickers, start=start_date, end=end_date, auto_adjust=True, actions=False)

print(f"Downloading market index data for {market_index_tickers} from {start_date} to {end_date}...")
# Download historical market index data
market_data = yf.download(market_index_tickers, start=start_date, end=end_date, auto_adjust=True, actions=False)

# Extract 'Close' prices for both stocks and market indices
stock_close = stock_data['Close']
market_close = market_data['Close']

# Forward-fill any missing values in the close price data.
# This is important for handling non-trading days for specific assets.
stock_close = stock_close.ffill()
market_close = market_close.ffill()

Calculate daily percentage returns
# .pct_change() calculates the percentage change between the current and a prior element.
# The first row will be NaN.
stock_daily_returns = stock_close.pct_change()
market_daily_returns = market_close.pct_change()

--- 4. Calculate Correlations ---

print("\nCalculating Pearson correlation coefficients...")
correlations = {}
for stock_ticker, market_ticker in stock_to_market_map.items():
    # Create a DataFrame combining daily returns for the current stock and its market index
    # This aligns the data by date and ensures only common dates are considered.
    combined_returns = pd.DataFrame({
        'stock_returns': stock_daily_returns[stock_ticker],
        'market_returns': market_daily_returns[market_ticker]
    }).dropna() # Drop rows with any NaN values (e.g., first day, market holidays)

    # Calculate Pearson correlation coefficient if there's enough data
    if not combined_returns.empty:
        correlation = combined_returns['stock_returns'].corr(combined_returns['market_returns'])
        correlations[stock_ticker] = correlation
    else:
        # Assign None or NaN if no common valid data points exist
        correlations[stock_ticker] = None

Print the calculated correlations
print('\nYearly Pearson Correlation Coefficients (2025):')
for stock, corr in correlations.items():
    if corr is not None:
        print(f'{stock}: {corr:.4f}')
    else:
        print(f'{stock}: Not enough data to calculate correlation')

--- 5. Generate Correlation Visualization ---

print("\nGenerating correlation visualization...")

Convert correlations dictionary to a Pandas Series for easier plotting
correlation_series = pd.Series(correlations).dropna() # Drop any None values

Sort the series for better visualization (highest correlation first)
correlation_series = correlation_series.sort_values(ascending=False)

Create a bar chart using seaborn and matplotlib
plt.figure(figsize=(12, 7)) # Set the figure size for better readability
sns.barplot(
    x=correlation_series.index,    # Stock tickers on the x-axis
    y=correlation_series.values,   # Correlation values on the y-axis
    hue=correlation_series.index,  # Use hue for distinct colors per bar
    palette='viridis',             # Color palette for the bars
    legend=False                   # Hide the legend as hue is used for x-labels
)

Add labels and title to the plot
plt.xlabel('Stock Ticker', fontsize=12)
plt.ylabel('Pearson Correlation Coefficient', fontsize=12)
plt.title('Stock vs. Market Index Correlation (2025)', fontsize=14)

Rotate x-axis labels for better readability, especially with longer tickers
plt.xticks(rotation=45, ha='right', fontsize=10) # 'ha' aligns text to the right of the tick
plt.yticks(fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7) # Add a subtle grid for readability

Adjust layout to prevent labels from overlapping
plt.tight_layout()

Display the plot
plt.show()

Pearson Correlation Coefficient Interpretation:
The Pearson correlation coefficient, ranging from -1 to +1, measures the linear relationship between two variables. In the context of stock returns and market indices:

High positive correlation (e.g., above 0.7): This indicates a strong tendency for the stock's daily returns to move in the same direction and with similar magnitude as the market index. Stocks with high positive correlation are highly sensitive to overall market movements, often implying they offer less diversification benefits against market-wide risks.

Moderate positive correlation (e.g., between 0.3 and 0.7): This suggests that the stock's returns generally move in the same direction as the market, but with less consistency or a lower magnitude of response. These stocks provide some exposure to market movements but might offer slightly more diversification than highly correlated assets.

Low positive correlation (e.g., between 0 and 0.3): A low positive correlation indicates a weak tendency for the stock's returns to move with the market. These stocks are less influenced by broad market swings and can be valuable for portfolio diversification, as their performance is less predictable based solely on market performance.

Negative correlation (e.g., below 0): This signifies that the stock's returns tend to move in the opposite direction to the market index. Such stocks are highly desirable for diversification, as they can help offset losses in a portfolio during market downturns. While theoretically beneficial, strong negative correlations are rare for most individual stocks relative to broad market indices.

Zero correlation: A correlation close to zero implies no linear relationship between the stock's returns and the market index returns. The stock's movements are largely independent of the market, offering significant diversification potential.


The script above provides a comprehensive solution for calculating and visualizing the Pearson correlation coefficients between a defined set of stocks and their respective market indices.

**How to Use:**
1.  **Copy and Paste**: Copy the entire code block into a new Python file (e.g., `stock_correlation_analysis.py`) or directly into a Colab/Jupyter Notebook cell.
2.  **Install Libraries**: If you don't have them, install the required libraries by running `pip install yfinance pandas matplotlib seaborn` in your terminal or a notebook cell.
3.  **Customize Inputs**: Modify the `stock_tickers`, `market_index_tickers`, `start_date`, `end_date`, and most importantly, the `stock_to_market_map` dictionary according to your specific analysis needs. Ensure that each stock in `stock_tickers` has a corresponding entry in `stock_to_market_map` pointing to a valid market index from `market_index_tickers`.
4.  **Run**: Execute the script. It will download the data, perform the calculations, print the correlations to the console, and display a bar chart visualizing these correlations.
