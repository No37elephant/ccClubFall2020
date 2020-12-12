# import sqlite3

# def read(db_file):
#     conn = sqlite3.connect(db_file)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * from demo")
#     values = cursor.fetchall()
#     for row in values:
#         print(row)
    
#     cursor.close()
#     conn.close()

# db_file = '/Users/hazel_lin/Desktop/Students.db'
# read(db_file)

# https://www.itread01.com/content/1544942735.html
# # Module Imports
# import mariadb
# import sys

# # Connect to MariaDB Platform
# try:
#     conn = mariadb.connect(
#         user = 'db_user',
#         password = 'db_user_passwd',
#         host = '192.0.2.1',
#         port = 3306,
#         database = 'employees'
#     )

# except mariadb.Error as e:
#     print(f'Error connecting to MariaDB Platform: {e}')
#     sys.exit(1)

# # Get Cursor
# cur = conn.cursor()

# https://stackoverflow.com/questions/10154633/load-csv-data-into-mysql-in-python
import csv
import mariadb
import pandas as pd

mydb = mariadb.connect(
    host = 'localhost',
    user = 'root',
    passwd='c923761997',
    db = 'extracted_geoinfo'
)
cur = mydb.cursor()
cur.execute("CREATE OR REPLACE DATABASE extracted_geoinfo \
    character set = 'utf8mb4' \
    collate = 'utf8mb4_general_ci'")

table_name = 'bar'
cur.execute("CREATE OR REPLACE TABLE extracted_geoinfo.bar \
    (name TEXT NOT NULL, \
    rating FLOAT NOT NULL, \
    address TEXT NOT NULL, \
    ave_price FLOAT NOT NULL, \
    url TEXT NOT NULL, \
    tel TEXT NOT NULL, \
    lat_lng TEXT NOT NULL, \
    place_id TEXT UNIQUE);")

# import csv files using pandas
df = pd.read_csv("1207_info.csv",sep=',', index_col = 0)
# print(df['url'])
# print(df.shape[0])
# for i in range(df.shape[0]):
#     # print(list(df.iloc[0,:].astype('str')))
#     row = df.iloc[i,:]
#     # print(row)
#     add = "INSERT INTO extracted_geoinfo.bar (name, rating, address, ave_price, url, tel, lat_lng, place_id ) \
#         VALUES({}, {}, {}, {}, {}, {}, {}, {});".format(str(row['name']), row['rating'], str(row['address']), row['ave_price'], str(row['url']), str(row['tel']),str(row['lat_lng']),str(row['place_id']))
#     cur.execute(add)

row_num = df.shape[0]
table_name = 'extracted_geoinfo.bar'

for n in range(row_num):
    lst = list(df.iloc[1,:].astype('str'))
    lst = ['\"' + n + '\"' for n in lst]

cur.execute("INSERT INTO {table_name}({columns})values({values});".format(
    table_name = table_name,
    columns = ', '.join(list(df.columns)),
    values = ', '.join(lst)
))

# close the connection to the database.
mydb.commit()
cur.close()
print('Done')

# 1212 
# Those as follow are good references for learning database/python interfaces. 
# https://www.datacamp.com/community/tutorials/mysql-python 
# https://www.techonthenet.com/mariadb/

# import pandas
# import mariadb
# import sys

# # connect to mariadb server, it is optional to set up db. One can create new one or modify existing one.
# # using the command of "mysql -u root -p -h localhost" to log in mariadb in your terminal

# try:
#     conn = mariadb.connect(
#         host = "localhost",
#         user = "root",
#         passwd = "c923761997",
#     )
# except mariadb.Error as e:
#     print(f"Error connecting to MariaDB Platform: {e}")
#     sys.exit(1) # exit(0):無錯誤退出; exit(1):有錯誤退出; 退出代碼是告訴編譯器的（或操作系統）

# # create interface between python and mariadb server using cursor
# cur = conn.cursor()

# # after the connection, we can use python code to construct or modify maria databases
# # by using .execute()
# # One can refer to https://www.techonthenet.com/mariadb/index.php for sql commands
# # Using the command of "show databases; " to check the exitstence of databases
# # Please do not forget the ";"

# cur.execute("CREATE DATABASE IF NOT EXISTS test_db \
#     character set = 'utf8mb4' \
#     collate = 'utf8mb4_general_ci'")

# # import csv files using pandas
# df = pandas.read_csv("1207_info.csv", sep = ',', index_col = 'name')

# # create table in your db, for example test_db in this case
# # using the commands of "use database_name; (you need to specify the name)" to log in the database.
# # then, using command of "describe table_name" to see tables in the related database

# table_name = 'test_db.test_table'
# cur.execute("CREATE OR REPLACE TABLE test_db.test_table \
#     (empty_var text not null);")

# # create column in table, namely test_table here
# for column in df:
#     cur.execute(f"alter table test_db.test_table \
#                 add {column} text not null;")

# cur.execute(f"ALTER TABLE {table_name} DROP column empty_var")
# # add data into corresponding columns in the related table

# row_num = df.shape[0]
# table_name = 'test_db.test_table'

# for n in range(row_num):
#     lst = list(df.iloc[1,:].astype('str'))
#     lst = ['\"' + n + '\"' for n in lst]

# cur.execute("INSERT INTO {table_name}({columns})values({values})".format(
#     table_name = table_name,
#     columns = ', '.join(list(df.columns)),
#     values = ', '.join(lst)
# ))

# # finally using the command of select * from table_name to see your input data,
# # after successfully executing conn.commit()
# conn.commit()

# cur.close()