import pandas as pd


def return_hyperlink(x):
    return '=HYPERLINK("{0}", {1})'.format(x['link'], x['price'])


outfile = '../../DATA/frap-ali-ozon-wb.csv'
out_xls = '../../DATA/pivot.xlsx'
df = pd.read_csv(outfile, delimiter=';', header=None,
                 names=['art', 'title', 'price', 'shop', 'link'])
df['shop_price'] = df.apply(return_hyperlink, axis=1)
dfp = pd.pivot_table(df,  index='art', values=['shop_price','link'], columns=['shop'], aggfunc='first', fill_value='-',)
#print(dfp.iloc[0, 3])
dfp.to_excel(out_xls)
