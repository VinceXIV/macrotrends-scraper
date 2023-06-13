from stocksymbol import StockSymbol
from scraper import scrape_financial_info
from ssk import ssk
import pandas as pd
import numpy as np

ssm = StockSymbol(ssk)

# Get tickers of companies listed in NASDAQ
symbol_list = ssm.get_symbol_list(market="US")
nasdaq_list = [x['symbol'] for x in symbol_list if x['exchange'] == 'NASDAQ']

# Get some of the important financial ratios
def get_ratios(ticker):
    financial_info = scrape_financial_info(ticker)

    financial_info['ebtda-margin'] = financial_info['ebitda'].astype(float) / financial_info['revenue'].astype(float)
    financial_info['gross-profit-margin'] = financial_info['gross-profit'].astype(float) / financial_info['revenue'].astype(float)
    financial_info['cogs-margin'] = financial_info['cost-goods-sold'].astype(float) / financial_info['revenue'].astype(float)
    financial_info['eps-basic-net-earnings-per-share'] = financial_info['eps-basic-net-earnings-per-share'].astype(float)
    financial_info['eps-earnings-per-share-diluted'] = financial_info['eps-earnings-per-share-diluted'].astype(float)

    return financial_info[
            [
                'ebtda-margin',
                'gross-profit-margin',
                'cogs-margin',
                'eps-basic-net-earnings-per-share',
                'eps-earnings-per-share-diluted' 
            ]]


# Make the values in a df to range between 0 and 1
def normalize(df):
    result = {}
    for col in df.columns:
        min_val = df[col].min()
        max_val = df[col].max()
        result[col] = df[col].apply(lambda x: (x - min_val)/(max_val - min_val))

    return pd.DataFrame(result)

# Calculate the score by calculating the product of all normalized
# value of the fundamental variable at each time
def get_score(ticker):
    ratios = normalize(get_ratios(ticker))
    score = ratios.apply(lambda row: np.prod(row), axis=1)

    # Adjust score such that the first value = 1
    first_val = score[0]
    return score / first_val
    