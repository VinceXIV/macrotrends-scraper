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
                yearly_data = data[data['year'] == year]
                end_date = yearly_data['Date'].max()
                start_date = yearly_data['Date'].min()

                start_adj_close = float(data[data['Date'] == start_date]['Adj Close'])
                end_adj_close = float(data[data['Date'] == end_date]['Adj Close'])

                year_return = (end_adj_close - start_adj_close)/start_adj_close

                result[ticker][year] = year_return
            except:
                continue

    return pd.DataFrame(result)

def get_monthly_return(ticker_list, start_year):
    result = {}
    for ticker in ticker_list:
        data = yf.download(ticker, progress=False).reset_index()
        data = data[data['Date'].dt.year >= start_year]
        data['year'] = data['Date'].dt.year
        data['month'] = data['Date'].dt.month

        result[ticker] = {}
        for year in data['year'].unique():
            try:
                yearly_data = data[data['year'] == year]

                for month in data['month'].unique():
                    monthly_data = yearly_data[yearly_data['month'] == month]

                    end_date = monthly_data['Date'].max()
                    start_date = monthly_data['Date'].min()

                    start_adj_close = float(data[data['Date'] == start_date]['Adj Close'])
                    end_adj_close = float(data[data['Date'] == end_date]['Adj Close'])

                    month_return = (end_adj_close - start_adj_close)/start_adj_close

                    result[ticker]["{y}-{m}".format(y=year, m=month)] = month_return
            except:
                continue   

    return pd.DataFrame(result)


# Returns price (Adj Close) relative to the first price
# Where the first price is set to 1
def get_monthly_adjusted_price(ticker_list, start_year):
    result = {}
    for ticker in ticker_list:
        data = yf.download(ticker, progress=False).reset_index()
        data = data[data['Date'].dt.year >= start_year]
        data['year'] = data['Date'].dt.year
        data['month'] = data['Date'].dt.month

        start_month_price = None

        result[ticker] = {}
        for year in data['year'].unique():
            try:
                yearly_data = data[data['year'] == year]

                for month in data['month'].unique():
                    monthly_data = yearly_data[yearly_data['month'] == month]
                    end_date = monthly_data['Date'].max()
                    end_adj_close = float(data[data['Date'] == end_date]['Adj Close'])

                    if start_month_price == None:
                        start_month_price = end_adj_close

                    adj_price = end_adj_close/start_month_price

                    result[ticker]["{y}-{m}".format(y=year, m=month)] = adj_price
            except:
                continue   

    return pd.DataFrame(result)