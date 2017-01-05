#Hybrid system
#Source: https://www.youtube.com/watch?v=9gBC9R-msAk
import numpy as np
from lightfm.datasets import fetch_movielens
from lightfm import LightFM
import pandas as pd
import pymysql
from sklearn.model_selection import train_test_split
from scipy.sparse import coo_matrix

def recommend(model_list, data, user):
	recMoviesByModel = {}
	recMovies = []

	# Split training/test data
	training_data, test_data = train_test_split(data, test_size=0.8)
	
	#number of users and movies in training data
	n_users, n_items = training_data.shape

	training_data = coo_matrix(training_data)
	test_data = coo_matrix(test_data)
	print(test_data)

	for model_name in model_list:
		#create model
		model = LightFM(loss=model_name)
		
		#train model
		model.fit(training_data, epochs=30, num_threads=2)

		#movies our model predicts they will like
		scores = model.predict(user, np.arange(n_items))
		
		#rank them in order of most liked to least
		top_items = data['movieId'][np.argsort(-scores)]
		
		#init empty list		
		movList = []
		for k, movie in enumerate(top_items[:30]):
			#Append movie to list and dict
			movList.append(movie)	
			recMovies.append(movie)
		#Append list to current model/user
		recMoviesByModel[modelName] = movList	
	

	return False#recMovies, recMoviesByModel	

def main():
	# Setup connection
	conn = pymysql.connect(host='81.204.145.155', user="dsMinor", passwd="dsMinor!123", db='MoviesDS', 
		charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

	#Load models
	model_list = ['warp', 'logistic', 'bpr', 'warp-kos']

	# Load ratings
	ratings = pd.read_sql("select * from ratings", con=conn)
	logged_in_user = 7	

	test = fetch_movielens()
	print(test['train'])

	# Get recommendations for each model 
	rec_movies_by_model = recommend(model_list, ratings, logged_in_user)

	return rec_movies_by_model

if __name__ == '__main__':
	data = main()
	#print(data)

#Register the number of occurances everytime the model is called. Then take the average at
# the end of the project. This will determine which model works best.

