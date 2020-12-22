# Host: ec2-54-211-99-192.compute-1.amazonaws.com
# Database: d9gnei48mbovh8
# User: fusoiorzocvqjt
# Port: 5432
# Password: f73bec6757bce818757e1a8894f40ca1a104ffa4459db7a62c424b71263b4bdd

import os
import re
import psycopg2
import pandas as pd
import numpy as np
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# DATABASE_URL = os.environ['postgres://fusoiorzocvqjt:f73bec6757bce818757e1a8894f40ca1a104ffa4459db7a62c424b71263b4bdd@ec2-54-211-99-192.compute-1.amazonaws.com:5432/d9gnei48mbovh8']

# conn = psycopg2.connect(DATABASE_URL, sslmode='require')
conn = psycopg2.connect(database='d9gnei48mbovh8', user='fusoiorzocvqjt', password='f73bec6757bce818757e1a8894f40ca1a104ffa4459db7a62c424b71263b4bdd', host='ec2-54-211-99-192.compute-1.amazonaws.com',port='5432')


cur = conn.cursor()
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
conn.set_client_encoding('UTF8')
cur.execute("GRANT ALL PRIVILEGES ON DATABASE d9gnei48mbovh8 TO fusoiorzocvqjt; \
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO fusoiorzocvqjt;")
cur.execute("ALTER DATABASE d9gnei48mbovh8;")

cur.execute("DROP TABLE IF EXISTS bar;")

table_name = 'bar'
cur.execute("CREATE TABLE bar \
    (name TEXT NOT NULL, \
    rating FLOAT NOT NULL, \
    address TEXT NOT NULL, \
    avg_price FLOAT NOT NULL, \
    url TEXT NOT NULL, \
    tel TEXT NOT NULL, \
    lat FLOAT NOT NULL, \
    lng FLOAT NOT NULL, \
    review TEXT NOT NULL, \
    place_id TEXT NOT NULL);")

# import csv files using pandas
df = pd.read_csv("all_bar.csv", index_col = 0)
df['tel'].replace(np.nan, 0, inplace = True)
df['lat'].replace('No latitude found!',0, inplace=True)
df['lng'].replace('No longitude found!',0, inplace=True)
df['avg_price'].replace(np.nan,0,inplace=True)
with open('all_bar.json', 'w', encoding='utf8') as f:
    f.write(df.to_json(orient='records', lines=False))

# row_num = df.shape[0]
# # print(row_num)

# for n in range(row_num):
#     lst = list(df.iloc[n,:].astype('str'))
#     # lst = ['\"' + n + '\"' for n in lst]
#     # print(', '.join(list(df.columns)))
#     table_name = table_name
#     # columns = "', '".join(list(df.columns))
#     # values = "', '".join(lst)
#     columns = ", ".join(list(df.columns))
#     values = ", ".join(lst)
#     # cur.execute("INSERT INTO bar (%s)values(%s);", 
#     #     (columns, values))
#     # print(lst[0])
#     cur.execute("INSERT INTO bar (name, rating, address, url, place_id, lat, lng, review, tel, avg_price)\
#         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", 
#         (lst[0],lst[1],lst[2],lst[3],lst[4],lst[5],lst[6],lst[7],lst[8],lst[9],))
# cur.execute("\SET content `cat /Users/hazel_lin/Documents/GitHub/ccClubFall2020/ccClub/all_bar.json` \
#     INSERT INTO bar VALUES(:'content');")

with open('all_bar.json') as file:
    # change json.load(file) to file.read()
    data = file.read()
# data.replace('No latitude found!',0, inplace=True)
# data.replace('No longitude found!',0, inplace=True)  
# re.sub('No latitude found!',0, data)
# re.sub('No longitude found!',0, data)
# just put a placeholder %s instead of using {} and .format().
query_sql="""INSERT INTO bar SELECT * FROM json_populate_recordset(NULL::bar, %s);"""
cur.execute(query_sql, (data,))

# close the connection to the database.
conn.commit()
cur.close()
print('Done')