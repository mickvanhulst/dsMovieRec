#Hybrid system
#Source: https://www.youtube.com/watch?v=9gBC9R-msAk
import numpy as np
from lightfm.datasets import fetch_movielens
from lightfm import LightFM
import pandas as pd

#fetch data and format it. Only take the higher ratings, since we want to recommend movies that users liked.
#Change data to dataset 
data = fetch_movielens(min_rating=3.5)

#Load models
modelList = ['warp', 'logistic', 'bpr', 'warp-kos']
user = 3

#recommendations dict -- ModelName | movieName
recMoviesByModel = {}

#Create empty list for movies
recMovies = []

def sample_recommendation(modelList, data, user_ids):
	#number of users and movies in training data
	n_users, n_items = data['train'].shape
	for i, modelName in enumerate(modelList):
		#create model
		model = LightFM(loss=modelName)
		#train model
		model.fit(data['train'], epochs=30, num_threads=2)

		#movies they already like
		known_positives = data['item_labels'][data['train'].tocsr()[user].indices]

		#movies our model predicts they will like
		scores = model.predict(user, np.arange(n_items))
		#rank them in order of most liked to least
		top_items = data['item_labels'][np.argsort(-scores)]
		
		#init empty list		
		movList = []
		for k, movie in enumerate(top_items[:30]):
			#Append movie to list and dict
			movList.append(movie)	
			recMovies.append(movie)
		#Append list to current model/user
		recMoviesByModel[modelName] = movList		

#Third parameter is the userId. So we have to replace that with the userId for who we are trying to recommend.  
sample_recommendation(modelList, data, user)

#Count amount of occurances
movTop = []
for mov in set(recMovies):
	movTop.append([mov, recMovies.count(mov)])

#Sort high/low and only keep values that occur more than one time
movTop = sorted(movTop, key=lambda x:x[1], reverse=True)

##Recommend movFiltered
movFiltered = list(filter(lambda x: x[1] > 1, movTop))

print(movFiltered)

##Determine accuracy
#Filter movies so that we just have the movienames
dictModelAcc = {}
justMov = [i[0] for i in movFiltered]
#Loop through dict and detect which algo holds the most of the filtered values.
for model in recMoviesByModel:
	dictModelAcc[model] = 0
	for index, item in enumerate(recMoviesByModel[model]):
		if item in justMov:
			dictModelAcc[model] += 1

#Print models with number of occurances
print(dictModelAcc)

#Register the number of occurances everytime the model is called. Then take the average at
# the end of the project. This will determine which model works best.