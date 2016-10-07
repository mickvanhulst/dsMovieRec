#Import packages
import pandas as pd
import pymysql
import sklearn.model_selection as sk

Connection = pymysql.connect(host='81.204.145.155', user="dsMinor", password="dsMinor!123", db='MoviesDS', charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

#Get keywords
mov = pd.read_sql("select * from movies", con=Connection)
ratings = pd.read_sql("select * from ratings", con=Connection)

#Merge sets
df = pd.merge(mov, ratings, how="left", on="movieId")

#Split test/training set
train, test = sk.train_test_split(df, test_size=0.2)

#Create dataframes
train = pd.DataFrame(train)
test = pd.DataFrame(test)

#Insert into database
#train.to_sql(con=Connection, name='trainSet', if_exists='replace', flavor='mysql', index=False)
#test.to_sql(con=Connection, name='testSet', if_exists='replace', flavor='mysql', index=False)

#Close connection
Connection.close()