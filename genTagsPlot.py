#Import packages
import pandas as pd # mov processing, CSV file I/O (e.g. pd.read_csv)
import omdb #Package used to scrape movie mov from API
import pymysql
from nltk.corpus import stopwords

Connection = pymysql.connect(host='81.204.145.155', user="dsMinor", password="dsMinor!123", db='MoviesDS', charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

#Get keywords
mov = pd.read_sql("select * from movies", con=Connection)

#Get stopwords for removal
stop = stopwords.words('english')

#Convert to lower case and remove special characters
mov['Plot'] = mov['Plot'].str.lower()
mov['Plot'] = mov['Plot'].str.replace('[^\w\s]','')

#Split keywords from plot
keywords = mov['Plot'].str.split(' ').apply(pd.Series, 1).stack()
keywords.index = keywords.index.droplevel(-1)

#Create dataframe and insert index column (movieTitle)
df = pd.DataFrame(keywords)

#Change column name
df.columns = ['Keyword'] #

#Add new columns to start of dataframe
df.insert(0, 'movieId', df.index) #reference to movies table
df.insert(0, 'genKeywordId', range(0, len(df))) #Will be used as unique key

#Remove stopwords and empty strings from dataframe
df = df[(~df['Keyword'].isin(stop)) & (df['Keyword'] != "")]

#Insert into database
df.to_sql(con=Connection, name='genKeywords', if_exists='replace', flavor='mysql', index=False)

#Close connection
Connection.close()