import sqlite3
import csv
import pandas as pd


#create_table = ''' CREATE TABLE IF NOT EXISTS people (
#                    id integer PRIMARY KEY
#                    firstName text
#                    lastName text
#                    phoneNumber integer
#                    memberID integer
#                    accountID integer
#'''

conn = sqlite3.connect('winston.db')
c = conn.cursor()

#c.execute(create_table)

data = pd.read_csv('./member_data.csv')
data.to_sql('people', conn, if_exists="replace",index=True)

conn.close()