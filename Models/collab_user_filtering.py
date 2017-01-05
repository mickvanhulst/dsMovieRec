import pandas as pd
import numpy as np
import pymysql
from collections import Counter
import operator

def top_k_movies(similarity, mapper, movie_idx, k=6):
	return [mapper[x] for x in np.argsort(similarity[movie_idx,:])[:-k-1:-1]]

def cos_similarity(ratings, epsilon=1e-9):
    # epsilon -> small number for handling dived-by-zero errors
	sim = ratings.T.dot(ratings) + epsilon
	norms = np.array([np.sqrt(np.diagonal(sim))])
	
	return (sim / norms / norms.T)

def process_data(conn):
	# Get data
	ratings = pd.read_sql("select * from ratings", con=conn)
	movies = pd.read_sql("select movieId, title from movies", con=conn)

	# Reset movie index
	movies['idx'] = movies.index

	# merge 
	merged_ratings = pd.merge(ratings, movies, on='movieId', how='left')

	#Get number of users/movies
	n_users = len(merged_ratings['userId'].unique())
	n_movies = len(movies['idx'].unique())

	#Matrix Factorize user x items
	ratings_matrix = np.zeros((n_users, n_movies))

	# Create matrix showing rating by user and movie
	for row in merged_ratings.itertuples():
		ratings_matrix[row[1]-1, row[6]-1] = row[3]

	# Get indexes with movie references
	idx_to_movie = {}

	for movie in merged_ratings['idx'].unique():
		idx_to_movie[movie] = movies.loc[movie, 'title']

	return ratings, movies, merged_ratings, n_users, n_movies, ratings_matrix, idx_to_movie

def get_recommendations(user, merged_ratings, item_correlation, idx_to_movie, movies):
	# Movies that user likes
	user = 670
	movies_logged_in_user = merged_ratings['idx'][merged_ratings['userId'] == user]

	#Find movies that similar uses like
	user_movies_dict = []
	for movie_idx in movies_logged_in_user:
		user_movies_dict.extend(top_k_movies(item_correlation, idx_to_movie, movie_idx))

	# Count movies
	count_movies = dict(Counter(user_movies_dict))
	total_movies = len(count_movies)

	# Keep top thirty percent
	count_movies = dict(sorted(count_movies.items(), 
		key=operator.itemgetter(1), reverse=True)[:round(total_movies * 0.3)])

	# Get movieId from movie name
	recommendations = movies['movieId'][movies['title'].isin(list(count_movies.keys()))]

	return list(recommendations.values)

def main(user):
	# Setup connection
	conn = pymysql.connect(host='81.204.145.155', user="dsMinor", passwd="dsMinor!123", db='MoviesDS', 
			charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	
	# Get processed data
	ratings, movies, merged_ratings, n_users, n_movies, ratings_matrix, idx_to_movie = process_data(conn)

	# Close connection
	conn.close()

	#Using cosine similarity to find similarity between items
	item_correlation = 1 - cos_similarity(ratings_matrix)

	# Get recommendations
	recommendations = get_recommendations(user, merged_ratings, item_correlation, idx_to_movie, movies)

	return recommendations

if __name__ == '__main__':
	user = 670
	data = main(user)
	print(data)