import pandas as pd
import copy

def get_pair_distance(df, start_year_month=None, end_year_month=None):
    '''
    Receives a dataframe with index being the date (could be years) and 
    columns are the stocks then calculates the spread using sum of squared distance
    '''

    if(start_year_month != None):
        df = df[df.index >= start_year_month]
    if(end_year_month != None):
        df = df[df.index < end_year_month]

    df = df.dropna(axis=1)

    df_ssd = {}

    # calculate the sum of squared difference for each column
    for stock_1 in df:
        df_ssd[stock_1] = {}
        for stock_2 in df:
            if stock_1 != stock_2:
                ssd = ((df[stock_1] - df[stock_2])**2).sum()
                df_ssd[stock_1][stock_2] = ssd

    df_ssd = pd.DataFrame(df_ssd)

    pairs = {}
    for col in df_ssd:
        for row in df_ssd.index:

            key = '_'.join([val for val in sorted([col, row])])

            # If we already have a pair (a, b), we don't want another
            # pair (b, a). We also don't want a pair of an asset and itself
            if(row != col and key not in pairs):
                pairs[key] = df_ssd[row][col]

    return pd.Series(pairs).sort_values(ascending=False)

def get_distance(df1, df2_list = [], start_year_month=None, end_year_month=None):
    # because we don't want to alter the original df1 sent in this function
    df = copy.deepcopy(df1)
    
    # because if column has all values as NaN, multiplying by others will result
    # in all of them having NaN
    df = df.dropna(axis=1, how='all')

    # We expect df1 and df2 to have the same column names with the content
    # being for different variables. For instance, one df will have information
    # about normalized ebtda-margin, while another will have information about
    # normalized cost of goods sold
    for df2 in df2_list:
        df2 = df2.dropna(axis=1, how='all')
        for column in df1:
            try:
                df[column] = df[column] * df2[column]
            except:
                continue

    return get_pair_distance(df, start_year_month, end_year_month)
