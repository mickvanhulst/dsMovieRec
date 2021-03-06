import pandas as pd
from pandas.io import sql
import pymysql
import omdb # Package used to scrape movie mov from API
from sqlalchemy.types import VARCHAR
from sqlalchemy import create_engine
import sqlalchemy
from nltk.corpus import stopwords
import nltk

#nltk.download()
# Connect to database
Connection = pymysql.connect(host='81.204.145.155', user="dsMinor", passwd="dsMinor!123", db='MoviesDS', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

# Create engine
engine = sqlalchemy.create_engine('mysql+pymysql://dsMinor:dsMinor!123@81.204.145.155/MoviesDS?charset=utf8', encoding="utf-8")

# Load dataframes
ratings = pd.read_csv('../data/ratings.csv', encoding='utf-8')
movies = pd.read_csv('../data/movies.csv', encoding='utf-8')

# Drop timestamp column
ratings = ratings.drop('timestamp', 1)

#### omdbApiScraper
# Remove year from title and strip spaces from sides
movies['title'] = movies['title'].str.replace(r"\(.*\)", "")
movies['title'] = movies['title'].str.strip()

# Create dataframe
columns_omdb = ['Title', 'Plot', 'Year', 'imdbID'
        , 'Director', 'Runtime', 'Language', 'Country', 'imdbRating', 'Actors', 'Awards']
df_omdb = pd.DataFrame(columns=columns_omdb)

for i in range(len(movies)):
    # Process API and create movframe
    print(i)
    request = omdb.request(t=movies['title'][i], r='json', fullplot=True).content
    
    # Jaar en eventuele andere kolommen toevoegen
    req = pd.DataFrame(eval(request), columns=columns_omdb, index=[0])
    
    #print(req)
    df_omdb = pd.DataFrame(df_omdb, columns=columns_omdb).append(req, ignore_index=True)

df_omdb = df_omdb.rename(columns = {'Title':'title'})
movies = pd.merge(left=movies, right=df_omdb, on='title', how='left')

# Insert movies in MySql
movies.to_sql(con=engine, name='movies', if_exists='append', index=False)

# Get stopwords for removal
stop = stopwords.words('english')

#Convert to lower case and remove special characters
movies['Plot'] = movies['Plot'].str.lower()
movies['Plot'] = movies['Plot'].str.replace('[^\w\s]', '')

# Split keywords from plot
keywords = movies['Plot'].str.split(' ').apply(pd.Series, 1).stack()
keywords.index = keywords.index.droplevel(-1)

# Create dataframe and insert index column (movieTitle)
gen_keywords = pd.DataFrame(keywords)

# Change column name
gen_keywords.columns = ['Keyword']

# Add movieId, start this value at one because of the dataset.
gen_keywords.insert(0, 'movieId', (gen_keywords.index + 1))

# Remove stopwords and empty strings from dataframe
gen_keywords = gen_keywords[(~gen_keywords['Keyword'].isin(stop)) & (gen_keywords['Keyword'] != "")]

# Insert into database
gen_keywords.to_sql(con=engine, name='genKeywords', if_exists='append', index=False)

# Insert into database
ratings.to_sql(con=engine, name='ratings', if_exists='append', index=False)

# Save all users from ratings in db.
users = pd.concat([pd.DataFrame(ratings['userId'].unique()), pd.DataFrame(ratings['userId'].unique()).astype(str)], axis=1)
users.columns = ['userId', 'username']
users.to_sql(con=engine, name='user', if_exists='append', index=False)

#Close connection
Connection.close()