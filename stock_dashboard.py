import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import yfinance as yf
import datetime

# Streamlit dashboard setup
st.title('Stock Dashboard')
ticker = st.sidebar.text_input('Ticker')

# Sidebar Date Input
start_date = st.sidebar.date_input('Start Date', datetime.datetime.now() - datetime.timedelta(days=30))  # Default to last month
end_date = st.sidebar.date_input('End Date', datetime.datetime.now())

# Sidebar Quick Date Range Buttons
st.sidebar.write("Quick Date Ranges:")
if st.sidebar.button('Last Week'):
    start_date = datetime.datetime.now() - datetime.timedelta(days=7)
    end_date = datetime.datetime.now()

if st.sidebar.button('Last Month'):
    start_date = datetime.datetime.now() - datetime.timedelta(days=30)
    end_date = datetime.datetime.now()

if st.sidebar.button('Last 3 Months'):
    start_date = datetime.datetime.now() - datetime.timedelta(days=90)
    end_date = datetime.datetime.now()

if st.sidebar.button('Last Year'):
    start_date = datetime.datetime.now() - datetime.timedelta(days=365)
    end_date = datetime.datetime.now()

def pricing_data_tab(data):
    with pricing_data:
        st.header('Price Movements')
        data2 = data.copy()
        data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1 
        data2.dropna(inplace=True)
        st.write(data2)
        annual_return = data2['% Change'].mean() * 252 * 100
        st.write('Annual Return is', annual_return, '%')
        stdev = np.std(data2['% Change']) * np.sqrt(252)
        st.write('Standard Deviation is', stdev * 100, '%')
        st.write('Risk Adj Return is', annual_return / (stdev * 100))

def fundamental_data_tab(ticker_info):
    with fundamental_data:
        # Fetching financial statements using yfinance
        balance_sheet = ticker_info.balance_sheet
        income_statement = ticker_info.financials
        cash_flow = ticker_info.cashflow

        # Display financial statements
        st.subheader('Balance Sheet')
        st.write(format_financial_statement(balance_sheet))

        st.subheader('Income Statement')
        st.write(format_financial_statement(income_statement))

        st.subheader('Cash Flow Statement')
        st.write(format_financial_statement(cash_flow))

def news_tab(company_news):
    with news:
        for i in range(len(company_news)):
            st.subheader(f'News {i+1}')
            publisher = company_news[i]['publisher']
            st.write(publisher)
            title = company_news[i]['title']
            st.write(title)
            link = company_news[i]['link']
            st.write(link)
            unix_timestamp = company_news[i]['providerPublishTime']
            readable_date = datetime.datetime.fromtimestamp(unix_timestamp)
            st.write(readable_date)

def about_tab():
    with about:
        st.subheader('About')
        st.write('This dashboard is developed by Mikael Boudzko.')
        st.write('LinkedIn: www.linkedin.com/in/mikaelboudzko')
        st.write('This application is a work in progress; errors may occur.')
        st.write('Currently working on fixing JSON error in Streamlit environment.')

def format_financial_statement(statement):
    statement = statement.transpose()
    cols = pd.Series(statement.columns)
    for dup in cols[cols.duplicated()].unique():
        cols[cols[cols == dup].index.values.tolist()] = [dup + '_' + str(i) if i != 0 else dup for i in range(sum(cols == dup))]
    statement.columns = cols
    return statement.iloc[1:]

def welcome_page():
    st.write('Welcome to the Stock Dashboard')
    st.write('Please input the ticker and set the date range in the side menu; when entering the ticker, press return/enter to save the ticker.')

if not ticker:
    welcome_page()
else:
    ticker_info = yf.Ticker(ticker)
    company_name = ticker_info.info['longName']
    company_news = ticker_info.news

    data = yf.download(ticker, start=start_date, end=end_date)
    fig = px.line(data, x=data.index, y='Adj Close', title=company_name)
    st.plotly_chart(fig)

    pricing_data, fundamental_data, news, about = st.tabs(['Pricing Data', 'Fundamental Data', 'News', 'About'])

    pricing_data_tab(data)
    fundamental_data_tab(ticker_info)
    news_tab(company_news)
    about_tab()
