import pandas as pd
import xlrd

df = pd.read_excel('data.xlsx')
print(df)
df.columns = ['price' , 'description']
print(df)
print(df.dtypes)

list = []
list2 = []
for value in df['price']:
    value = str(value)
    value = value.replace(".", "")
    value = value.replace(",", ".")
    value = int(value)
    list.append(value)
for title in df['description']:
    title = str(title)
    list2.append(title)
d = {'price':list,'description':list2}
df2 = pd.DataFrame(d)
print(df2)
print(df2.dtypes)

df2 = df2.sort_values(by='price')
df2.reset_index(drop=True,inplace=True)
print(df2)
