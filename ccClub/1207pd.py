# import csv
# import pandas as pd
# import numpy as np

# first_df = pd.read_csv('1213_info.csv', index_col = 0)
# print(first_df['ave_price'])
# first_df.rename(columns={'Unnamed: 0.1':'index'})
# first_df.drop(columns=['Unnamed: 0'],inplace=True)

# print(first_df.columns)
# first_df.to_csv('1213_info.csv', index=False)

# r[['lat','lng']] = pd.DataFrame(r.tolist(), index=r.index)
# print(r)


# second_df = pd.read_csv('1213_info.csv')
# second_df.rename(columns={'Unnamed: 0.1':'index'})
# second_df.to_csv('1213_info.csv', index=False)

# import csv
# import sqlite3

# def dataImport(csvpath, dbpath, tablename):
#     reader = csv.DictReader(open(csvpath, '/Users/hazel_lin/Documents/GitHub/1207_info.csv'), delimeter=',',quoting=csv.QUOTE_MINIMAL)
#     conn = sqlite3.connect(dbpath)
#     # fix error with non-ASCII input
#     conn.text_factory = str
#     c = conn.cursor()
#     create_query = 'CREATE TABLE '+ tablename +'(name TEXT NOT NULL,rating FLOAT NOT NULL,address TEXT NOT NULL, ave_price FLOAT NOT NULL, url TEXT NOT NULL, tel TEXT NOT NULL, lat_lng TEXT NOT NULL, place_id TEXT UNIQUE)'
#     c.execute(create_query)
#     for row in reader:
#         print (row)
#         to_db = [row['name'],row['rating'],row['address'],row['ave_price'],row['url'],row['tel'],row['lat_lng'],row['place_id']]
#         c.execute('INSERT INTO '+bar+'(name, rating, address, ave_price, url, tel, lat_lng, place_id')
#     conn.commit()
# print('Done')

# import json
# import csv
# import pandas as pd
# df = pd.read_json('Tainan_city.json')
# df.to_csv('bar_tainan.csv', encoding = 'utf8')
# df = pd.read_csv('bar_tainan.csv', index_col=0)
# df = df.rename(columns={'avg_price':'ave_price'})
# df.to_csv('bar_tainan.csv', encoding = 'utf8')

# def tidy_up(x):
#     x = x.replace('$','')
#     x = x.replace('以下','')
#     x = int(x)
#     return x

# df['ave_price1'] = df['ave_price'].apply(tidy_up)
# print(df['ave_price1'])
# df.drop(columns=['ave_price'],inplace=True)
# df = df.rename(columns={'ave_price1':'ave_price'})
# df.to_csv('bar_tainan.csv', encoding = 'utf8')

# print(type(df['rating'].iloc[1]))
# print(type(df['coordinates'].iloc[0]))
# def tidy_up(x):
#     x = x.replace('{','')
#     x = x.replace('}','')
#     x = x.replace("'lat':",'')
#     x = x.replace("'lng':",'')
#     x = x.replace(' ','')
#     result = x.split(',')
#     return result
# df['lat_lng'] = df['coordinates'].apply(tidy_up)
# # print(type(df['lat_lng'].iloc[0]))
# df[['lat','lng']] = pd.DataFrame(df.lat_lng.to_list(), index = df.index)
# # print(df)
# df.drop(columns=['lat_lng'], inplace = True)

# # print(type(df['tel'].iloc[0]))
# def tidy_up(x):
#     x = str(x)
#     x = x.replace('.0','')
#     # result = '0' + x
#     return x
# df['tel'] = df['tel'].apply(tidy_up)
# # print(df['tel'])
# # print(df['tel_new'])
# # df.drop(columns=['tel'], inplace=True)
# # df = df.rename(columns={'tel_new':'tel'})

# df.to_csv('bar_tainan.csv', encoding = 'utf8')

import pandas as pd
import csv

db1 = pd.read_csv('1213_info.csv',index_col=0)
db2 = pd.read_csv('bar_tainan.csv',index_col=0)

db3 = pd.concat([db1,db2],join='outer')
# print(db3)
db3.to_csv('1217test.csv', encoding='utf8')