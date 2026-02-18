# --- 1. Import necessary libraries ---
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 2. Define user input variables ---
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

# --- 3. Implement Data Download and Preprocessing ---

print(f"Downloading stock data for {stock_tickers} from {start_date} to {end_date}...")
stock_data = yf.download(stock_tickers, start=start_date, end=end_date, auto_adjust=True, actions=False)

print(f"Downloading market index data for {market_index_tickers} from {start_date} to {end_date}...")
market_data = yf.download(market_index_tickers, start=start_date, end=end_date, auto_adjust=True, actions=False)

stock_close = stock_data['Close']
market_close = market_data['Close']

stock_close = stock_close.ffill()
market_close = market_close.ffill()

# Calculate daily percentage returns
stock_daily_returns = stock_close.pct_change()
market_daily_returns = market_close.pct_change()

# --- 4. Calculate Correlations ---

print("\nCalculating Pearson correlation coefficients...")
correlations = {}
for stock_ticker, market_ticker in stock_to_market_map.items():
    combined_returns = pd.DataFrame({
        'stock_returns': stock_daily_returns[stock_ticker],
        'market_returns': market_daily_returns[market_ticker]
    }).dropna()

    if not combined_returns.empty:
        correlation = combined_returns['stock_returns'].corr(combined_returns['market_returns'])
        correlations[stock_ticker] = correlation
    else:
        correlations[stock_ticker] = None

# Print the calculated correlations
print('\nYearly Pearson Correlation Coefficients (2025):')
for stock, corr in correlations.items():
    if corr is not None:
        print(f'{stock}: {corr:.4f}')
    else:
        print(f'{stock}: Not enough data to calculate correlation')

# --- 5. Generate Correlation Visualization ---

print("\nGenerating correlation visualization...")

# Convert correlations dictionary to a Pandas Series for easier plotting
correlation_series = pd.Series(correlations).dropna()

# Sort the series for better visualization (highest correlation first)
correlation_series = correlation_series.sort_values(ascending=False)

# Create a bar chart using seaborn and matplotlib
plt.figure(figsize=(12, 7))
sns.barplot(
    x=correlation_series.index,
    y=correlation_series.values,
    hue=correlation_series.index,
    palette='viridis',
    legend=False
)

# Add labels and title to the plot
plt.xlabel('Stock Ticker', fontsize=12)
plt.ylabel('Pearson Correlation Coefficient', fontsize=12)
plt.title('Stock vs. Market Index Correlation (2025)', fontsize=14)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Adjust layout to prevent labels from overlapping
plt.tight_layout()

# Display the plot
plt.show()
