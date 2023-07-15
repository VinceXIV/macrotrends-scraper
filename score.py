from stocksymbol import StockSymbol
from scraper import scrape_financial_info
import pandas as pd
import numpy as np

def get_ratio(row, col_1, col_2):
    try:
        return float(row[col_1]) / float(row[col_2])
    except:
        return np.nan

def get_ratios(ticker):
    financial_info = scrape_financial_info(ticker)

    financial_info['ebtda-margin'] = financial_info.apply(lambda row: get_ratio(row, 'ebtda', 'revenue'), axis=1)

    financial_info['gross-profit-margin'] = financial_info.apply(lambda row: get_ratio(row, 'gross-profit', 'revenue'), axis=1)
    financial_info['cogs-margin'] = financial_info.apply(lambda row: get_ratio(row, 'cost-goods-sold', 'revenue'), axis=1)
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

    score = score.sort_index(ascending=True)
    return score
    
def clean_scores(scores):
    # Because most scores don't have a value in 2023 yet
    scores = scores[scores.index < 2023]


    return scores.dropna(axis=1)

def get_scores_df(ticker_list, method=np.sum, limit=np.inf):
    scores = []
    for ticker, i in zip(ticker_list, range(len(ticker_list))):
        try:
            scores.append(get_score(ticker, method=method))
        except:
            continue

        if(i >= limit):
            break

    return clean_scores(pd.concat(scores, axis=1))