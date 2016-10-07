#Import packages
import pandas as pd
import pymysql

Connection = pymysql.connect(host='81.204.145.155', user="dsMinor", password="dsMinor!123", db='MoviesDS', charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

#Get keywords
mov = pd.read_sql("select * from movies", con=Connection)
ratings = pd.read_sql("select * from ratings", con=Connection)

#Merge sets
df = pd.merge(mov, ratings, how="left", on="movieId")

#Split test/training set

#Insert into database
#df.to_sql(con=Connection, name='genKeywords', if_exists='replace', flavor='mysql', index=False)


#Close connection
Connection.close()