#######################################################################################################

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as ta

import datetime
import datetime as dt
import datetime as d
import pytz

# Set the desired time zone (Indian Standard Time)
indian_timezone = pytz.timezone('Asia/Kolkata')

# Get the current time in the Indian time zone
current_time = dt.datetime.now(indian_timezone)#.strftime("%H:%M:%S")
today= d.datetime.today().date()#.strftime("%Y-%m-%d") 

end_date = datetime.datetime.now() + datetime.timedelta(days=1)
# Function to fetch 1-min live data
start_date = end_date - datetime.timedelta(days=5)

def fetch_data(ticker,time_frame):
    # Download the historical data for Bank Nifty with a 1-minute interval
    data = yf.download(tickers=ticker, start=start_date, end=current_time, interval=time_frame)
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
    df['Close_4']=df['Close'].shift(4)
    # Determine bullish or bearish condition
    df['Condition'] = 'Neutral'
    df.loc[((df['RSI'] > 85) & ((df['Close_0']>df['Close_1']) &(df['Close_1']>df['Close_2']) &(df['Close_2']>df['Close_3'])&(df['Close_3']>df['Close_4']))), 'Condition'] = 'Bullish'
    df.loc[((df['RSI'] < 15)& ((df['Close_0']<df['Close_1']) &(df['Close_1']<df['Close_2']) &(df['Close_2']<df['Close_3'])&(df['Close_3']<df['Close_4']))), 'Condition'] = 'Bearish'
    df['Datetime']=pd.to_datetime(df.index)
    # print(df.tail())
    # df.index=df['Datetime'].dt.tz_convert(None)
    df_bullish = df[(df['Condition']=='Bullish') ]
    df_bearish = df[(df['Condition']=='Bearish') ]
    return df_bullish, df_bearish
top_10_stocks = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS', 'ADANIPORTS.NS', 'ICICIBANK.NS', 'KOTAKBANK.NS', 'SBIN.NS', 'BAJFINANCE.NS']

nifty_100_stocks = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS",
    "ICICIBANK.NS", "KOTAKBANK.NS", "ITC.NS", "SBIN.NS",
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
    "LTI.NS", "MPHASIS.NS", "MRF.NS", "NAUKRI.NS", "PFC.NS", "TRENT.NS","INDHOTEL.NS","JKCEMENT.NS","CHAMBLFERT.NS"
]


st.set_page_config(layout="wide")
st.title('2RSI Scanner Streamlit App')
def app(data_bull,data_bear):
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
    #selected_date = st.selectbox("Select Date", unique_dates,index=1)
    most_recent_date = max(unique_dates)
    selected_date = st.radio("Select Any Date :",unique_dates,horizontal=True,index=np.argmax(np.array(unique_dates)))
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

def process_all_stocks(stocks_list,time_frame):
    all_data_bulish = []  # List to store data from all stocks
    all_data_bearish = []
    for symbol in stocks_list:
        data = fetch_data(symbol,time_frame)
        if not data.empty:
            data_bulish, data_bearish = compute_indicators(data)
            data_bulish['Symbol'] = symbol[:-3]  # Add a column to identify the stock symbol
            data_bearish['Symbol'] = symbol[:-3] 
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
    selected_TF = st.radio("Select Any TF :",['5m'],horizontal=True)
    data_bull,data_bear = process_all_stocks(nifty_100_stocks,selected_TF)
    if not data_bull.empty:
        app(data_bull,data_bear)
        # print(merged_data.tail(10))

    else:
        print("No data available for any of the symbols.")

# Run the main function

if __name__ == "__main__":

    main()
    # app()
