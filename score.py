from stocksymbol import StockSymbol
from scraper import scrape_financial_info
import pandas as pd
import numpy as np
import copy

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
    for col, i in zip(df.columns, range(len(df.columns))):
        first_val = df.iloc[0, i]
        result[col] = df[col].apply(lambda x: x/first_val)

    return pd.DataFrame(result)

# Calculate the score
def get_score(ticker, method=np.sum, use = None):
    ratios = normalize(get_ratios(ticker))

    # Person may only need to one column (e.g ebtda-margin)
    # in that case, they will pass an array of what they want
    # if they are not specific about what they want. We 
    # give them everything
    if(not use):
        use = ['ebtda-margin', 'gross-profit-margin','cogs-margin', 'eps-earnings-per-share-diluted']

    # Create a list of items for which we would like to calculate the spread
    # of the assets using the sum of squared distance method
    # In the first round, it would simply be the variables, e.g 'ebtda-margin',
    # 'gross-profit-margin', etc. Then everything combined
    fundamentals = {}
    for col in use:
        fundamentals[col] = [col]
    fundamentals['all-fundamental-variables'] = copy.deepcopy(use)

    scores = {}
    for val in fundamentals:
        score = ratios[fundamentals[val]].apply(lambda row: method(row), axis=1)

        # Pick only the year (as integer) for index
        score = score.reset_index()
        score['year'] = score['index'].apply(lambda x: int(x.split("-")[0]))
        score = score.set_index('year')

        # Drop duplicated indices
        # Read more about it here; https://stackoverflow.com/questions/13035764/remove-pandas-rows-with-duplicate-indices
        score = score[~score.index.duplicated(keep='first')]

        # Convert score to dataframe and use ticker name as column name
        score = pd.DataFrame(score)[[0]]
        score.rename(columns={0: ticker}, inplace=True)

        # Normalize the score such that the first value = 1 and all the
        # rest are relative to it
        first_year_raw_score = score.sort_index(ascending=True).iloc[0]
        score[ticker] = score[ticker].apply(lambda x: x/first_year_raw_score)

        scores[val] = score.sort_index(ascending=True)

    return scores
    
def clean_scores(scores):
    # Because most scores don't have a value in 2023 yet
    scores = scores[scores.index < 2023]

    return scores

def get_scores_df(ticker_list, method=np.sum, limit=np.inf, use=None):
    scores = {}
    for ticker, i in zip(ticker_list, range(len(ticker_list))):
        try:
            score_val = get_score(ticker, method=method, use=use)
            for key in score_val:
                if key in scores:
                    scores[key].append(score_val[key])
                else:
                    scores[key] = []
                    scores[key].append(score_val[key])
        except:
            continue

        if(i >= limit):
            break

    print("scores: ", scores)
    result = {}
    for key in scores:
        result[key] = clean_scores(pd.concat(scores[key], axis=1))

    return result