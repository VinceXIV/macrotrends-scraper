import pandas as pd

def get_pair_distance(df, start_year_month=None, end_year_month=None):
    if(start_year_month != None):
        df = df[df.index >= start_year_month]
    if(end_year_month != None):
        df = df[df.index < end_year_month]

    df_corr = df.dropna(axis=1).corr()

    pairs = {}
    for col in df_corr:
        for row in df_corr.index:

            key = '_'.join([val for val in sorted([col, row])])

            # If we already have a pair (a, b), we don't want another
            # pair (b, a). We also don't want a pair of an asset and itself
            if(row != col and key not in pairs):
                pairs[key] = df_corr[row][col]

    return pd.Series(pairs).sort_values(ascending=False)