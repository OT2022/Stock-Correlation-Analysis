# Stock-Correlation-Analysis
Example Stock Correlation Analysis script to calculate a stock's correlation to its respective market index over a specific time period.

Very basic script but the idea is that you can use it to enter a ticker and market index for a specific time period (by updating the start_date and end_date variable) to pull the daily returns for the stock and market index. The correlation is then calculated using Pearson Correlation coefficient. The daily price returns are downloaded using yahoo finance.

Pearson Correlation Coefficient Interpretation:
The Pearson correlation coefficient, ranging from -1 to +1, measures the linear relationship between two variables. In the context of stock returns and market indices:

High positive correlation (e.g., above 0.7): This indicates a strong tendency for the stock's daily returns to move in the same direction and with similar magnitude as the market index. Stocks with high positive correlation are highly sensitive to overall market movements, often implying they offer less diversification benefits against market-wide risks.

Moderate positive correlation (e.g., between 0.3 and 0.7): This suggests that the stock's returns generally move in the same direction as the market, but with less consistency or a lower magnitude of response. These stocks provide some exposure to market movements but might offer slightly more diversification than highly correlated assets.

Low positive correlation (e.g., between 0 and 0.3): A low positive correlation indicates a weak tendency for the stock's returns to move with the market. These stocks are less influenced by broad market swings and can be valuable for portfolio diversification, as their performance is less predictable based solely on market performance.

Negative correlation (e.g., below 0): This signifies that the stock's returns tend to move in the opposite direction to the market index. Such stocks are highly desirable for diversification, as they can help offset losses in a portfolio during market downturns. While theoretically beneficial, strong negative correlations are rare for most individual stocks relative to broad market indices.

Zero correlation: A correlation close to zero implies no linear relationship between the stock's returns and the market index returns. The stock's movements are largely independent of the market, offering significant diversification potential.
