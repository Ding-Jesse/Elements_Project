# read_e2k()
# read_rebar_excel()
# combine_both()
# output_e2k()
from e2k import write_e2k
from rebar_excel import read_rebar_excel,rename_unnamed,sortarea
def main():
    pass
    df = read_rebar_excel('data/BigBeamA號數轉換_V2.4.xlsx')
    df = rename_unnamed(df)
    df.fillna('', inplace=True)
    sortarea(df)
    write_e2k(df,'data/2022-0110_ShyueShyh_A2.e2k','data/','output.e2k')
main()
