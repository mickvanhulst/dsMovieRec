#Import packages
import pandas as pd # mov processing, CSV file I/O (e.g. pd.read_csv)
import omdb #Package used to scrape movie mov from API
import pymysql
from nltk.corpus import stopwords

Connection = pymysql.connect(host='127.0.0.1', user="root", db='test', charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

#Get keywords
mov = pd.read_sql("select * from movies", con=Connection)

#Get stopwords for removal
stop = stopwords.words('english')

#Convert to lower case and remove special characters
mov['title'] = mov['title'].str.lower()
mov['title'] = mov['title'].str.replace('[^\w\s]','')

#Split keywords from plot
keywords = mov['title'][0:10].str.split(' ').apply(pd.Series, 1).stack()
keywords.index = keywords.index.droplevel(-1)

#Create dataframe and insert index column (movieTitle)
df = pd.DataFrame(keywords)

#Set column name
df.columns = ['Keyword']

#Add new columns to start of dataframe
df.insert(0, 'movieId', df.index)
df.insert(0, 'genKeywordId', range(0, len(df)))

#Remove stopwords from dataframe
df = df[~df['Keyword'].isin(stop)]

#Insert into database
df.to_sql(con=Connection, name='genKeywords', if_exists='replace', flavor='mysql', index=False)

#Close connection
Connection.close()
