import pandas as pd
from pandas.io import sql
import pymysql

#connect to database
Connection = pymysql.connect(host='127.0.0.1', user="root", db='test', charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

csvNames = {'movies', 'links', 'tags', 'ratings'}

#Loop through data files and export to MySQL db
for csv in csvNames:
    file = pd.read_csv('./data/' + csv + '.csv')
    file.to_sql(con=Connection, name=''+csv+'', if_exists='replace', flavor='mysql')

#Close connection
Connection.close()