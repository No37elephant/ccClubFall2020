import os
import psycopg2

conn = psycopg2.connect(database='d9gnei48mbovh8', user='fusoiorzocvqjt', password='f73bec6757bce818757e1a8894f40ca1a104ffa4459db7a62c424b71263b4bdd', host='ec2-54-211-99-192.compute-1.amazonaws.com',port='5432')
cursor = conn.cursor()

cursor.execute("SELECT * FROM bar")

data = []
while True:
    temp = cursor.fetchone()
    if temp:
        data.append(temp)
    else:
        break
print(data)

cursor.close()

# data = []
# while True:
#     temp = cursor.fetchone()
#     if temp:
#         data.append(temp)
#     else:
#         break
# print(data)