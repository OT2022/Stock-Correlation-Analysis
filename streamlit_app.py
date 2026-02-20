import streamlit as st
import pandas as pd
import yfinance as yf

st.title("Relative Value: Correlation Tool")
st.caption("Note: Only UK (.L), German (.DE), French (.PA), and US (.US) tickers are currently supported. More countries to be added soon.")

# User input
ticker = st.text_input("Enter Ticker e.g. VOD.L, SAP.DE, OR.PA, AMZN.US", "VOD.L")
start_date = st.text_input("Enter start date e.g. 2025-01-01", "2025-01-01")
end_date = st.text_input("Enter end date e.g. 2025-12-31", "2025-12-31")

# Map ticker to index and prepare ticker for yfinance download
if ".L" in ticker:
    index = '^FTSE'
    download_ticker = ticker
elif ".DE" in ticker:
    index = '^GDAXI'
    download_ticker = ticker
elif ".PA" in ticker:
    index = '^FCHI'
    download_ticker = ticker
elif ".US" in ticker:
    index = '^GSPC'
    download_ticker = ticker.replace('.US', '') # Remove .US suffix for yfinance
else:
    st.error("Ticker is not currently available. Please use a ticker ending in '.L' for UK stocks, '.DE' for German stocks, '.PA' for French stocks, or '.US' for US stocks.")
    st.stop() # Stop execution if ticker format is not supported

# Calculation logic
# We use an 'if' statement for the button to trigger calculations
if st.button('Calculate Correlation'):
    # Download data using the specified ticker (which might have had its suffix removed) and index, and dates
    data = yf.download([download_ticker, index], start=start_date, end=end_date)
    data_adj = data['Close']

    # Check if data was actually returned from yfinance
    if not data_adj.empty:
        # 1. Calculate the Rebased series (Start at 100) to visualize relative performance
        rebased_data = (data_adj / data_adj.iloc[0]) * 1
        # Calculate daily percentage returns and drop any NaN values (e.g., first day)
        price_return = data_adj.pct_change().dropna()

        # Check if the specific ticker column exists in price_return
        if download_ticker in price_return.columns:
            # Calculate Pearson correlation between stock returns and market index returns
            correlation = price_return[download_ticker].corr(price_return[index])

            # Display the calculated correlation as a Streamlit metric
            st.metric(label=f"Correlation: {ticker} vs {index}", value=f"{correlation:.2f}")

            # Display the rebased performance data as a line chart
            st.subheader("Relative Performance")
            st.line_chart(rebased_data)
        else:
            st.error(f"Data for ticker {download_ticker} not found in downloaded data. Please check the ticker symbol.")
    else:
        # Display an error message if no data was found
        st.error("No data found for those dates or tickers. Please check the ticker symbol and date range.")
