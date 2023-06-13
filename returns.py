import pandas as pd
import yfinance as yf

def get_yearly_return(ticker_list, start_year):
    result = {}
    for ticker in ticker_list:
        data = yf.download(ticker, progress=False).reset_index()
        data = data[data['Date'].dt.year >= start_year]
        data['year'] = data['Date'].dt.year

        result[ticker] = {}
        for year in data['year'].unique():
            try:
                data_year = data[data['year'] == year]
                end_date = data_year['Date'].max()
                start_date = data_year['Date'].min()

                start_adj_close = float(data[data['Date'] == start_date]['Adj Close'])
                end_adj_close = float(data[data['Date'] == end_date]['Adj Close'])

                year_return = (end_adj_close - start_adj_close)/start_adj_close

                result[ticker][year] = year_return
            except:
                continue

    return pd.DataFrame(result)