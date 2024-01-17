import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import yfinance as yf
import datetime

#streamlit run stock_dashboard.py

def format_financial_statement(statement):
    # Transpose the statement
    statement = statement.transpose()

    # Rename columns to ensure uniqueness
    cols = pd.Series(statement.columns)
    for dup in cols[cols.duplicated()].unique():
        cols[cols[cols == dup].index.values.tolist()] = [dup + '_' + str(i) if i != 0 else dup for i in range(sum(cols == dup))]
    
    statement.columns = cols

    # Return the formatted statement excluding the first row which is now headers
    return statement.iloc[1:]


# Streamlit dashboard setup
st.title('Stock Dashboard')
ticker = st.sidebar.text_input('Ticker')
ticker_info = yf.Ticker(ticker)
company_name = ticker_info.info['longName']
company_news = ticker_info.news
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')


# if not ticker:
#     st.write('Hello world') 
# else:
#     # Fetch and plot stock price data
#     data = yf.download(ticker, start=start_date, end=end_date)
#     fig = px.line(data, x=data.index, y='Adj Close', title=company_name)
#     st.plotly_chart(fig)

# Tabs setup
pricing_data, fundamental_data, news, about = st.tabs(['Pricing Data', 'Fundamental Data', 'News', 'About'])

with pricing_data:
    st.header('Price Movements')
    data2 = data
    data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1 
    data2.dropna(inplace = True)
    st.write(data2)
    annual_return = data2['% Change'].mean()*252*100
    st.write('Annual Return is', annual_return, '%')
    stdev = np.std(data2['% Change'])*np.sqrt(252)
    st.write('Standard Deviation is', stdev*100, '%')
    st.write('Risk Adj Return is', annual_return/(stdev*100))
    

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

# from stocknews import StockNews
# with news:
#     st.header(f'News of {company_name}')
#     sn = StockNews("MSFT", save_news=False)
#     df_news = sn.read_rss()
#     for i in range(10):
#         st.subheader(f'News {i+1}')
#         st.write(df_news['published'][i])
#         st.write(df_news['title'][i])
#         st.write(df_news['summary'][i])
#         title_sentiment = df_news['sentiment_title'][i]
#         st.write(f'Title Sentiment {title_sentiment}')
#         news_sentiment = df_news['sentiment_summary'][i]
#         st.write(f'News Sentiment {news_sentiment}')

with about: 
    st.subheader(f'Developed by Mikael Boudzko')
    st.write(f'1/09/2024 - Present')
    st.write(f'Linkedin: www.linkedin.com/in/mikaelboudzko')
    st.weite(f'Github repository: ')
