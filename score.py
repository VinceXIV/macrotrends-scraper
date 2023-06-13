from stocksymbol import StockSymbol
from scraper import scrape_financial_info
import pandas as pd
import numpy as np

# Get some of the important financial ratios
def get_ratios(ticker):
    financial_info = scrape_financial_info(ticker)

    financial_info['ebtda-margin'] = financial_info['ebitda'].astype(float) / financial_info['revenue'].astype(float)
    financial_info['gross-profit-margin'] = financial_info['gross-profit'].astype(float) / financial_info['revenue'].astype(float)
    financial_info['cogs-margin'] = financial_info['cost-goods-sold'].astype(float) / financial_info['revenue'].astype(float)
    # financial_info['eps-basic-net-earnings-per-share'] = financial_info['eps-basic-net-earnings-per-share'].astype(float)
    financial_info['eps-earnings-per-share-diluted'] = financial_info['eps-earnings-per-share-diluted'].astype(float)

    return financial_info[
            [
                'ebtda-margin',
                'gross-profit-margin',
                'cogs-margin',
                # 'eps-basic-net-earnings-per-share',
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

# Calculate the score
def get_score(ticker, method=np.sum):
    ratios = normalize(get_ratios(ticker))
    score = ratios.apply(lambda row: method(row), axis=1)

    # Pick only the year (as integer) for index
    score = score.reset_index()
    score['year'] = score['index'].apply(lambda x: int(x.split("-")[0]))
    score = score.set_index('year')

    # Convert score to dataframe and use ticker name as column name
    score = pd.DataFrame(score)[[0]]
    score.rename(columns={0: ticker}, inplace=True)

    # Adjust score such that the first value = 1
    first_year_raw_score = score.sort_index(ascending=True).iloc[0]
    score[ticker] = score[ticker].apply(lambda x: x/first_year_raw_score)

    return score
    

def get_scores_df(ticker_list, method=np.sum, limit=np.inf):
    scores = []
    for ticker, i in zip(ticker_list, range(len(ticker_list))):
        try:
            scores.append(get_score(ticker, method=method))
        except:
            continue

        if(i >= limit):
            break

    return pd.concat(scores, axis=1)