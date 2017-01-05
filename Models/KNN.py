import pandas as pd
import math
import numpy as np
import operator
import pymysql
 
# Turn off annoying warning (Link: http://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas)
pd.options.mode.chained_assignment = None

# Use root mean squared error, because the closer the user is, the smaller the rmse.
# - Always gives positive number
# - Emphasizes bigger deviations
def RMSE(user, ratings, ratings_log_in_user):
	max_rating = 5.0
	sum = 0
	count = 0
	log_in_user_movies = list(ratings_log_in_user['movieId'].values)

	# Loop through user rows
	for idx in ratings[ratings['userId'] == user].index:
		# If movie in ratings list of user
		movieId = ratings.loc[idx, 'movieId'].item()

		if movieId in log_in_user_movies:
			# Rating logged in user for current movie
			rating_curr_user = ratings_log_in_user['rating'][ratings_log_in_user['movieId'] == movieId]
			
			sum += math.pow(rating_curr_user - ratings.loc[idx, 'rating'].item(), 2)
			count += 1
		
	
	if not count:
		return 100000 # no ratings in common, so we return a huge distance
	else:
		return np.sqrt(sum / float(count)) + (max_rating / count)
		

def det_nearest_neighbours(ratings, ratings_log_in_user, k):
	# Loop through all and calculate RMSE
	dist_dict = {}

	for user in ratings['userId'].unique():
		# Set index of training point plus euclidean distance
		dist_dict[user] = RMSE(user, ratings, ratings_log_in_user)

	# Get k lowest values
	dict_top_k = sorted(dist_dict, key=dist_dict.get)[:k]

	return dict_top_k

def get_recommendations(ratings, ratings_log_in_user, nearest_neighbours):
	recommendations = {}

	# Get all movies from logged in user
	movies_log_in_user = list(ratings_log_in_user['movieId'].values)
	
	for neighbour in nearest_neighbours:
		for movie in ratings[ratings['userId'] == neighbour].index:
			movie_name = ratings.loc[movie, 'movieId']

			if movie_name not in movies_log_in_user:
				# Check if key exists, else init.
				if movie_name in recommendations:
					recommendations[movie_name] += 1
				else:
					recommendations[movie_name] = 1

	# Get sorted (high/low) movies where count higher than 1
	recommendations = dict((k, v) for k, v in recommendations.items() if v >= 1)

	return recommendations


def KNN(ratings, ratings_log_in_user, k):
	# Find k number of nearest neighbours
	nearest_neighbours = det_nearest_neighbours(ratings, ratings_log_in_user, k)

	# Get recommendations
	recommendations = get_recommendations(ratings, ratings_log_in_user, nearest_neighbours)
				
	return recommendations


def main():
	# Setup connection
	conn = pymysql.connect(host='81.204.145.155', user="dsMinor", passwd="dsMinor!123", db='MoviesDS', 
		charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

	# Get userId from form
	logged_in_user = 670

	# Load ratings
	ratings = pd.read_sql("select * from ratings", con=conn)

	# Determine k = n^0.5
	k = int(math.pow(len(ratings.index), 0.5))

	# Ratings current user
	ratings_log_in_user = ratings[ratings['userId'] == logged_in_user]

	# Generate recommendations
	recommendations = KNN(ratings, ratings_log_in_user, k)

	# Sort data and get top thirty percent
	recommendations = sorted(recommendations, key=recommendations.get, 
		reverse=True)[:round(len(recommendations) * 0.3)]

	return recommendations

if __name__ == '__main__':
	data = main()
	print(data)