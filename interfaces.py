import streamlit as st
import pandas as pd 
import yfinance as yf
import plotly.express as px

# import plotly.graph_objects as go
# get the tickers of commonly known stocks from the wedb and store them in a list all capitalized

def get_tickers():
    df = pd.read_csv('https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv')
    tickers = df['Symbol'].tolist()
    tickers = [ticker.upper() for ticker in tickers]
    index_sector = ['XLK', 'XLF', 'XLY', 'XLP', 'XLE', 'XLB', 'XLI', 'XLV', 'XLU']
    # get the tickers from the updated_stock_list.csv file and store them in a list
    csvdf = pd.read_csv('Updated_stock_list.csv')
    # get the tickers from the Ticker column and store them in a list
    csv_tickers = csvdf["Ticker "].tolist()
    tickers = tickers + index_sector + csv_tickers
    # reomve duplicates
    tickers = list(dict.fromkeys(tickers))
    return tickers


st.title('Stock Market Analysis')
start_date = st.date_input('Start Date', pd.to_datetime('2010-01-01'))
end_date = st.date_input('End Date', pd.to_datetime('today'))
dropmenu = st.multiselect('Select the stocks you want to analyze', get_tickers())

def relative_return(df):

    
    df = df['Adj Close'].pct_change()
    cumret = (1 + df).cumprod()-1
    cumret = cumret.fillna(0)
    # combine all dataframes into one
    return cumret

def get_support_resistance(df):
    if df.empty:
        return None
    else:
        df = df['Adj Close']
    # get the support and resistance lines for the stock data and return both as a a dataframe with the data's index
    # support and resistance lines the slope of the line of the df
    # get the slope of the line
        slope = df.diff()
        # get the support and resistance lines
        support = slope[slope < 0]
        resistance = slope[slope > 0]
        support = df.rolling(window=20).min()
        resistance = df.rolling(window=20).max()
        # rename support and resistance columns
        support = support.rename('Support')
        resistance = resistance.rename('Resistance')

        # combine adj close, support and resistance into one dataframe with date as index
        df = pd.concat([df, support, resistance], axis=1)
        return df
@st.cache
def get_data(ticker):
    data = yf.download(ticker, start_date, end_date)
    return data
if len(dropmenu) > 0:
    data = get_data(dropmenu)
    st.header("Relative Returns")
    # display charts with 1.5 width and center the x placement
    st.plotly_chart(px.line(relative_return(data), width=1500, template='plotly_dark', title='Relative Returns'), use_container_width=True)



    

# use y as the 3 column in the dataframe

