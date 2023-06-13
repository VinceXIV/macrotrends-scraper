import pandas as pd

def get_pair_distance(df, start_year_month=None, end_year_month=None):
    if(start_year_month != None):
        df = df[df.index >= start_year_month]
    if(end_year_month != None):
        df = df[df.index < end_year_month]

    df_corr = df.dropna(axis=1).corr()
    print(df_corr)

    pairs = {}
    for col in df_corr:
        for row in df_corr.index:
            if(row != col and (col, row) not in pairs):
                pairs[(row, col)] = df_corr[row][col]

    return pd.Series(pairs).sort_values(ascending=False)