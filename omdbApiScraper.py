#Import packages
import pandas as pd # mov processing, CSV file I/O (e.g. pd.read_csv)
import omdb #Package used to scrape movie mov from API
import pymysql
from sqlalchemy.types import VARCHAR

Connection = pymysql.connect(host='127.0.0.1', user="root", db='test', charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

mov = pd.read_sql("select * from movies", con=Connection)

#Remove year from title and strip spaces from sides
mov['title'] = mov['title'].str.replace(r"\(.*\)","")
mov['title'] = mov['title'].str.strip()

#Create new column and set index
mov['Plot'] = mov.index

for i in range(len(mov)):
    print(i)
    #Process API and create movframe
    request = omdb.request(t=mov['title'][i], r='json', fullplot=True, ).content
    dfPlot = pd.DataFrame(eval(request), columns=['Plot'], index=[0])
    dfPlot.index.name = 'Index'

    # Add values to dataframe and remove json brackets
    mov['Plot'][i] = list(map(str, dfPlot['Plot'].values))
    mov['Plot'][i] = ", ".join(mov['Plot'][i]) #Remove json brackets
    

#Insert df in MySql
mov.to_sql(con=Connection, name='movies', if_exists='replace', flavor='mysql', dtype={'Plot': 'VARCHAR(255)'})

#Close connection
Connection.close()