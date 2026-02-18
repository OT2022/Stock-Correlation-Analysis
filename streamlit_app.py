import streamlit as st
import pandas as pd
import yfinance as yf

st.title("Relative Value: Correlation Tool")

# User input
ticker = st.text_input("Enter Ticker e.g. VOD.L, BP.L, LLOY.L", "VOD.L")
start_date = st.text_input("Enter start date e.g. 2025-01-01", "2025-01-01")
end_date = st.text_input("Enter end date e.g. 2025-12-31", "2025-12-31")

# Map ticker to index
if ".L" in ticker:
    index = '^FTSE'
else:
    st.error("Ticker is not currently available")
    st.stop() 

# Calculation logic
# We use an 'if' statement for the button
if st.button('Calculate Correlation'):
    # Download data using the variables
    data = yf.download([ticker, index], start=start_date, end=end_date)
    data_adj = data['Close']
    
    # Check if data was actually returned
    if not data_adj.empty:
        # 1. Calculate the Rebased series (Start at 100)
        rebased_data = (data_adj / data_adj.iloc[0]) * 1
        # Calculate returns
        price_return = data_adj.pct_change().dropna()
        
        # Calculate correlation
        correlation = price_return[ticker].corr(price_return[index])

        # User output
        st.metric(label=f"Correlation: {ticker} vs {index}", value=f"{correlation:.2f}")
        
        # Display the chart
        st.subheader("Relative Performance")
        st.line_chart(rebased_data)
    else:
        st.error("No data found for those dates or tickers.")




                       
