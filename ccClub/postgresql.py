# Host: ec2-54-211-99-192.compute-1.amazonaws.com
# Database: d9gnei48mbovh8
# User: fusoiorzocvqjt
# Port: 5432
# Password: f73bec6757bce818757e1a8894f40ca1a104ffa4459db7a62c424b71263b4bdd

import os
import psycopg2
import pandas as pd
import csv
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
    ave_price FLOAT NOT NULL, \
    url TEXT NOT NULL, \
    tel TEXT NOT NULL, \
    lat FLOAT NOT NULL, \
    lng FLOAT NOT NULL, \
    place_id TEXT NOT NULL);")

# import csv files using pandas
df = pd.read_csv("1213_info.csv",sep=',', index_col = 0)
df['ave_price'].replace(np.nan, 0, inplace = True)


row_num = df.shape[0]
# print(row_num)

for n in range(row_num):
    lst = list(df.iloc[n,:].astype('str'))
    # lst = ['\"' + n + '\"' for n in lst]
    # print(', '.join(list(df.columns)))
    table_name = table_name
    # columns = "', '".join(list(df.columns))
    # values = "', '".join(lst)
    columns = ", ".join(list(df.columns))
    values = ", ".join(lst)
    # cur.execute("INSERT INTO bar (%s)values(%s);", 
    #     (columns, values))
    # print(lst[0])
    cur.execute("INSERT INTO bar (name, rating, address, ave_price, url, tel, place_id, lat, lng)\
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);", 
        (lst[0],lst[1],lst[2],lst[3],lst[4],lst[5],lst[6],lst[7],lst[8],))



# close the connection to the database.
conn.commit()
cur.close()
print('Done')