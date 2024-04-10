# import tkinter as tk
# from tkinter import ttk
# from tkinterhtml import HtmlFrame
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots

# class CandlestickChartApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Candlestick Chart App")
        
#         # Create GUI components
#         self.label_symbol = ttk.Label(self.root, text="Symbol:")
#         self.label_symbol.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
#         self.entry_symbol = ttk.Entry(self.root)
#         self.entry_symbol.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
#         self.button_generate = ttk.Button(self.root, text="Generate Chart", command=self.generate_chart)
#         self.button_generate.grid(row=0, column=2, padx=5, pady=5)
        
#         self.chart_container = HtmlFrame(self.root, width=800, height=600)
#         self.chart_container.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        
#     def generate_chart(self):
#         symbol = self.entry_symbol.get()
#         if not symbol:
#             tk.messagebox.showerror("Error", "Please enter a symbol.")
#             return
        
#         # Mock data for demonstration
#         data = {
#             'Date': ['2024-04-01', '2024-04-02', '2024-04-03', '2024-04-04'],
#             'Open': [100, 110, 105, 108],
#             'High': [120, 115, 112, 115],
#             'Low': [95, 105, 100, 103],
#             'Close': [110, 112, 107, 110]
#         }
        
#         # Create candlestick chart
#         fig = make_subplots(rows=1, cols=1)
#         fig.add_trace(go.Candlestick(x=data['Date'],
#                                       open=data['Open'],
#                                       high=data['High'],
#                                       low=data['Low'],
#                                       close=data['Close'],
#                                       name=symbol),
#                       row=1, col=1)
        
#         fig.update_layout(title=f'Candlestick Chart for {symbol}',
#                           xaxis_title='Date',
#                           yaxis_title='Price')
        
#         # Convert Plotly figure to HTML and render it in the chart container
#         chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
#         self.chart_container.set_content(chart_html)
        
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = CandlestickChartApp(root)
#     root.mainloop()





#######################################################################################################

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as ta

# Function to fetch 1-min live data
def fetch_data(ticker):
    data = yf.download(tickers=ticker, period="5d", interval="1m")
    return data

# Hull Moving Average
def HMA(df, window):
    weight = np.arange(1, window + 1)
    wma = df.rolling(window).apply(lambda prices: np.dot(prices, weight) / weight.sum(), raw=True)
    return wma

def round_2(x):
    try:
        return round(x,2)
    except:
        return x

@st.cache_data
def compute_indicators(df):
    # Calculate EMA and HMA
    df['EMA'] = ta.ema(df['Close'], 21)
    df['HMA'] = ta.hma(df['Close'], 51)
    
    # Supertrend (simplified version)
    # supertrend = ta.supertrend(df['Close'], 3, 7, 21, True)
    # df['Supertrend'] = supertrend.stc()
    
    # VWAP
    df['VWAP'] = ta.vwap(df['High'], df['Low'], df['Close'], df['Volume'],anchor='D')
    
    # RSI
    df['RSI'] = ta.rsi(df['Close'], 14)
    df['Close_0']=df['Close'].copy()
    df['Close_1']=df['Close'].shift(1)
    df['Close_2']=df['Close'].shift(2)
    df['Close_3']=df['Close'].shift(3)
    # df['Close_4']=df['Close'].shift(4)
    # Determine bullish or bearish condition
    df['Condition'] = 'Neutral'
    df.loc[((df['RSI'] > 85) & ((df['Close_0']>df['Close_1']) &(df['Close_1']>df['Close_2']) &(df['Close_2']>df['Close_3']))), 'Condition'] = 'Bullish'
    df.loc[((df['RSI'] < 15)& ((df['Close_0']<df['Close_1']) &(df['Close_1']<df['Close_2']) &(df['Close_2']<df['Close_3']))), 'Condition'] = 'Bearish'
    df['Datetime']=pd.to_datetime(df.index)
    # print(df.tail())
    # df.index=df['Datetime'].dt.tz_convert(None)
    df_bullish = df[(df['Condition']=='Bullish') ]
    df_bearish = df[(df['Condition']=='Bearish') ]
    return df_bullish, df_bearish
top_10_stocks = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS', 'ADANIPORTS.NS', 'ICICIBANK.NS', 'KOTAKBANK.NS', 'SBIN.NS', 'BAJFINANCE.NS']

nifty_100_stocks = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS",
    "HDFC.NS", "ICICIBANK.NS", "KOTAKBANK.NS", "ITC.NS", "SBIN.NS",
    "BHARTIARTL.NS", "ASIANPAINT.NS", "HCLTECH.NS", "WIPRO.NS", "DMART.NS",
    "LT.NS", "BAJFINANCE.NS", "AXISBANK.NS", "MARUTI.NS", "ULTRACEMCO.NS",
    "ONGC.NS", "SUNPHARMA.NS", "NTPC.NS", "TITAN.NS", "TECHM.NS",
    "POWERGRID.NS", "NESTLEIND.NS", "BAJAJFINSV.NS", "HINDZINC.NS", "INDUSINDBK.NS",
    "CIPLA.NS", "DRREDDY.NS", "GRASIM.NS", "JSWSTEEL.NS", "TATAMOTORS.NS",
    "TATASTEEL.NS", "BPCL.NS", "COALINDIA.NS", "HDFCLIFE.NS", "ADANIPORTS.NS",
    "HEROMOTOCO.NS", "HINDALCO.NS", "IOC.NS", "SBILIFE.NS", "UPL.NS",
    "SHREECEM.NS", "EICHERMOT.NS", "BAJAJ-AUTO.NS", "BRITANNIA.NS", "DIVISLAB.NS",
    "ZEEL.NS", "TATACONSUM.NS", "M&M.NS", "GAIL.NS", "BHARATFORG.NS",
    "PIDILITIND.NS", "SIEMENS.NS", "ICICIPRULI.NS", "LUPIN.NS", "MARICO.NS",
    "PGHH.NS", "DABUR.NS", "GODREJCP.NS", "BANDHANBNK.NS", "TATAPOWER.NS",
    "HDFCAMC.NS", "COLPAL.NS", "BERGEPAINT.NS", "ICICIGI.NS", "MUTHOOTFIN.NS",
    "NMDC.NS", "ACC.NS", "BIOCON.NS", "APOLLOHOSP.NS", "AMBUJACEM.NS",
    "AUROPHARMA.NS", "BOSCHLTD.NS", "HAVELLS.NS", "PEL.NS", "ASHOKLEY.NS",
    "CADILAHC.NS", "ADANIGREEN.NS", "ADANITRANS.NS", "LTTS.NS", "SRF.NS",
    "PIIND.NS", "JUBLFOOD.NS", "DLF.NS", "HINDPETRO.NS", "IGL.NS",
    "LTI.NS", "MPHASIS.NS", "MRF.NS", "NAUKRI.NS", "PFC.NS"
]
# Define custom CSS for changing text color

from st_aggrid import AgGrid

st.set_page_config(layout="wide")
def app(data_bull,data_bear):
    st.title('2RSI Scanner Streamlit App')

    # Convert 'Date' column to datetime format and extract date component
    data_bull['Date'] = pd.to_datetime(data_bull.index).date
    data_bull['Time'] = pd.to_datetime(data_bull.index).time
    # Convert 'Date' column to datetime format and extract date component
    data_bear['Date'] = pd.to_datetime(data_bear.index).date
    data_bear['Time'] = pd.to_datetime(data_bear.index).time
    # Get unique dates
    unique_dates = data_bull['Date'].unique()

    # data_bull.index=data_bull['Time']
    # data_bull=data_bull.sort_index()
    data_bull.reset_index(drop=True, inplace=True)
    # data_bear.index=data_bear['Time']#pd.to_datetime().strftime('%m-%d %H:%M')
    # data_bear=data_bear.sort_index()
    data_bear.reset_index(drop=True, inplace=True)
    # Display selectbox in Streamlit
    selected_date = st.selectbox("Select Date", unique_dates)
    # st.write("Selected Date:", selected_date)
    col1, col2 = st.columns(2)
    with col1:
        data_bull_date=data_bull[data_bull['Date']==selected_date]
        st.write("Bulish Signal Conditions:",selected_date)
        if len(data_bull_date)>0:
            st.dataframe(data_bull_date[['Time','Close','RSI','Symbol']].style.set_properties(**{'color': 'green'}).format({"Close": "{:.2f}","RSI": "{:.2f}"}),width=500) #.style.format({"Close": "{:.2f}","RSI": "{:.2f}"})
        else : 
            st.write("No Data")
    with col2:
        data_bear_date=data_bear[data_bear['Date']==selected_date]
        st.write("Bearish Signal Conditions:",selected_date)
        st.dataframe(data_bear_date[['Time','Close','RSI','Symbol']].style.set_properties(**{'color': 'red'}).format({"Close": "{:.2f}","RSI": "{:.2f}"}),width=500)
    # else:
    #     st.write("No data found for the symbol.")



# Assuming fetch_data and compute_indicators are defined elsewhere

def process_all_stocks(stocks_list):
    all_data_bulish = []  # List to store data from all stocks
    all_data_bearish = []
    for symbol in stocks_list:
        data = fetch_data(symbol)
        if not data.empty:
            data_bulish, data_bearish = compute_indicators(data)
            data_bulish['Symbol'] = symbol  # Add a column to identify the stock symbol
            data_bearish['Symbol'] = symbol 
            all_data_bulish.append(data_bulish)
            all_data_bearish.append(data_bearish)
        else:
            print(f"No data found for {symbol}.")  # Adjusted for a non-Streamlit context

    # Concatenate all the DataFrames in the list into a single DataFrame
    if all_data_bulish and all_data_bearish:
        final_df_bulish = pd.concat(all_data_bulish)
        final_df_bearish = pd.concat(all_data_bearish)
        return final_df_bulish,final_df_bearish
    else:
        return pd.DataFrame() ,pd.DataFrame # Return an empty DataFrame if no data was processed

# Function to run in a non-Streamlit environment (for demonstration)
def main():
    data_bull,data_bear = process_all_stocks(top_10_stocks)
    if not data_bull.empty:
        app(data_bull,data_bear)
        # print(merged_data.tail(10))

    else:
        print("No data available for any of the symbols.")

# Run the main function

if __name__ == "__main__":

    main()
    # app()
