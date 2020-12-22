import os
import psycopg2
# import numpy as np
import random
from random import randint

conn = psycopg2.connect(database='d9gnei48mbovh8', user='fusoiorzocvqjt', password='f73bec6757bce818757e1a8894f40ca1a104ffa4459db7a62c424b71263b4bdd', host='ec2-54-211-99-192.compute-1.amazonaws.com',port='5432')
cursor = conn.cursor()


# cursor.execute("SELECT * FROM bar;")
# cursor.execute("SELECT * FROM bar WHERE bar.ctid=%s::regclass;", (random.randint(1, 740),))
# cursor.execute("SELECT * FROM bar TABLESAMPLE SYSTEM(5);")
cursor.execute("SELECT * FROM bar order by random() limit 1000;")

data = []
x = 1
while x>0:
    temp = cursor.fetchone()
    # print("type="+ f'{type(temp)}')
    if temp:
        data.append(temp)
    else:
        break
    x -=1
# print(data[0][0], data[0][9], data[0][2], data[0][3])
print(data[0][0], data[0][2])

# data = []
# while True:
#     temp = cursor.fetchone()
#     if temp:
#         data.append(temp)
#     else:
#         break
# print(data)

cursor.close()

# data = []
# while True:
#     temp = cursor.fetchone()
#     if temp:
#         data.append(temp)
#     else:
#         break
# print(data)