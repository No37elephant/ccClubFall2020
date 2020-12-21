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
# df = pd.read_json('高雄市.json') # 台北市: ValueError: Trailing data
# df.to_csv('bar_kaohsiung.csv', encoding = 'utf8')
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
import numpy as np

db = pd.read_csv('all_bar.csv', index_col=0)

db.drop(columns=['avg_price'], inplace = True)
db.drop(columns=['coordinates'], inplace = True)
db = db.rename(columns={'ave_price':'avg_price'})

def tidy_up_tel(x):
    x = str(x)
    x = x.replace('nan','')
    x = x.replace('.0','')
    # result = int(x)
    return x
db['tel'] = db['tel'].apply(tidy_up_tel)

db.to_csv('all_bar.csv', encoding='utf8')

# def tidy_up_tel(x):
#     x = str(x)
#     x = x.replace('nan','')
#     x = x.replace('.0','')
#     # result = int(x)
#     return x
# db['tel'] = db['tel'].apply(tidy_up_tel)

# def tidy_up_price(x):
#     x = str(x)
#     x = x.replace('均消','')
#     return x
    # if x == float:
    #     return x
    # elif x == 'nan' or '':
    #     return x
    # else:
    #     x = str(x)
    #     x = x.replace('$','')
    #     x = x.replace('以上','')
    #     x = x.replace('以下','')
    #     return x
# db['ave_price'] = db['ave_price'].apply(tidy_up_price)
# # for row in range(138, 148):
# #     print(type(db['avg_price'][row]))
# db.to_csv('all_bar.csv', encoding='utf8')

# db = pd.concat([left, right], join='outer')
# print(df['ave_price1'])
# db.drop(columns=['coordinates'],inplace=True)
# db.to_csv('1220_test.csv', encoding='utf8')

# db1 = pd.read_csv('bar_changhua.csv',index_col=0)
# db2 = pd.read_csv('bar_chiayi.csv',index_col=0)
# db3 = pd.read_csv('bar_hsinchu.csv',index_col=0)
# db4 = pd.read_csv('bar_hsinchucity.csv',index_col=0)
# db5 = pd.read_csv('bar_kaohsiung.csv',index_col=0)
# db6 = pd.read_csv('bar_keelung.csv',index_col=0)
# db7 = pd.read_csv('bar_kinmeng.csv',index_col=0)
# db8 = pd.read_csv('bar_miaoli.csv',index_col=0)
# db9 = pd.read_csv('bar_nantou.csv',index_col=0)
# db10 = pd.read_csv('bar_newtaipei.csv',index_col=0)
# db11 = pd.read_csv('bar_penghu.csv',index_col=0)
# db12 = pd.read_csv('bar_pingtung.csv',index_col=0)
# db13 = pd.read_csv('bar_taichung.csv',index_col=0)
# db14 = pd.read_csv('bar_tainan.csv',index_col=0)
# db15 = pd.read_csv('bar_taipei.csv',index_col=0)
# db16 = pd.read_csv('bar_taitung.csv',index_col=0)
# db17 = pd.read_csv('bar_taoyuan.csv',index_col=0)
# db18 = pd.read_csv('bar_yilan.csv',index_col=0)
# db19 = pd.read_csv('bar_yunlin.csv',index_col=0)


# db = pd.concat([db1,db2,db3,db4,db5,db6,db7,db8,db9,db10,db11,db12,db13,db14,db15,db16,db17,db18,db19],join='outer',ignore_index=True)
# # # print(db3)
# db.to_csv('all_bar.csv', encoding='utf8')