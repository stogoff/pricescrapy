import pandas as pd


def return_hyperlink(x):
    return '=HYPERLINK("{0}", {1})'.format(x['link'], x['price'])


df = pd.read_csv('static/test.csv', delimiter=';', header=None,
                 names=['art', 'title', 'price', 'shop', 'link'])
df['linkedprice'] = df.apply(return_hyperlink, axis=1)

dfp = pd.pivot_table(df, values=['linkedprice'], index='art', columns='shop', aggfunc='first')

print(dfp.iloc[0, 3])

dfp.to_excel("output.xlsx")
