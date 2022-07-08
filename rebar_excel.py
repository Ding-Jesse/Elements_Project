import pandas as pd
import numpy as np
import rebar
import pprint
def read_rebar_excel(read_file):
    return pd.read_excel(
        read_file, sheet_name='輸出表',header=[0,1])

def rename_unnamed(df:pd.DataFrame):
    """Rename unamed columns name for Pandas DataFrame

    See https://stackoverflow.com/questions/41221079/rename-multiindex-columns-in-pandas

    Parameters
    ----------
    df : pd.DataFrame object
        Input dataframe

    Returns
    -------
    pd.DataFrame
        Output dataframe

    """
    for i, columns in enumerate(df.columns.levels):
        columns_new = columns.tolist()
        for j, row in enumerate(columns_new):
            if "Unnamed: " in row:
                columns_new[j] = ""
        if pd.__version__ < "0.21.0":  # https://stackoverflow.com/a/48186976/716469
            df.columns.set_levels(columns_new, level=i, inplace=True)
        else:
            df = df.rename(columns=dict(zip(columns.tolist(), columns_new)),
                           level=i)
    return df


def sortarea(df:pd.DataFrame):
    # out_df = pd.DataFrame(columns={'樓層','編號','左As','中As','右As'})
    for row in range(0,df.shape[0]-1,4):
        df.at[row,('主筋','左上As')] = gettotalarea(df.at[row,('主筋', '左1')],df.at[row+1,('主筋', '左1')])
        df.at[row,('主筋','中上As')] = gettotalarea(df.at[row,('主筋', '中')],df.at[row+1,('主筋', '中')])
        df.at[row,('主筋','右上As')] = gettotalarea(df.at[row,('主筋', '右1')],df.at[row+1,('主筋', '右1')])
        df.at[row,('主筋','左下As')] = gettotalarea(df.at[row+2,('主筋', '左1')],df.at[row+3,('主筋', '左1')])
        df.at[row,('主筋','中下As')] = gettotalarea(df.at[row+2,('主筋', '中')],df.at[row+3,('主筋', '中')])
        df.at[row,('主筋','右下As')] = gettotalarea(df.at[row+2,('主筋', '右1')],df.at[row+3,('主筋', '右1')])
        df.at[row,('主筋','左下長度')] = df.at[row+3,('主筋長度', '左1')]
        df.at[row,('主筋','中下長度')] = df.at[row+3,('主筋長度', '中')]
        df.at[row,('主筋','右下長度')] = df.at[row+3,('主筋長度', '右1')]
        df.at[row,('箍筋','左Avs')] = getstrriuparea(df.at[row,('箍筋',  '左')])
        df.at[row,('箍筋','中Avs')] = getstrriuparea(df.at[row,('箍筋',  '中')])
        df.at[row,('箍筋','右Avs')] = getstrriuparea(df.at[row,('箍筋',  '右')])
    pprint.pprint(df)

def gettotalarea(f_rebar,s_rebar):
    f_rebar_area = 0
    s_rebar_area = 0
    if f_rebar != 0:
        f_rebar_area = int(f_rebar.split('-')[0])*(rebar.rebar_area(f_rebar.split('-')[1]))*10000
    if s_rebar != 0:
        s_rebar_area = int(s_rebar.split('-')[0])*(rebar.rebar_area(s_rebar.split('-')[1]))*10000
    return f_rebar_area + s_rebar_area
def getstrriuparea(shear_rebar):
    return rebar.strriup_area(shear_rebar.split('@')[0])/(int(shear_rebar.split('@')[1])/100)
if __name__ == "__main__":
    df = read_rebar_excel('data/test_BigBeamA號數轉換_V2.4.xlsx')
    df = rename_unnamed(df)
    print(df)
    sortarea(df)
    df.to_excel("output.xlsx",sheet_name='Sheet_name_1')

