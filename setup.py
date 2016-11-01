import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances

#Functions


def predict_topk(ratings, similarity, k=50):
	pred = np.zeros(ratings.shape)
	for j in range(ratings.shape[1]):
		top_k_items = [np.argsort(similarity[:,j])[:-k-1:-1]]
		for i in range(ratings.shape[0]):
			pred[i, j] = similarity[j, :][top_k_items].dot(ratings[i, :][top_k_items].T) 
			pred[i, j] /= np.sum(np.abs(similarity[j, :][top_k_items])) 
	return pred

def top_k_movies(similarity, mapper, movie_idx, k=6):
	return [mapper[x] for x in np.argsort(similarity[movie_idx,:])[:-k-1:-1]]

#Reading ratings file:
r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
df = pd.read_csv('./data2/u.data', sep='\t', names=r_cols,
 encoding='latin-1')

#Get number of users
n_users = df.user_id.unique().shape[0]
n_items = df.movie_id.unique().shape[0]

#Matrix Factorize user x items
ratings = np.zeros((n_users, n_items))

#Fill matrix with rating given by user for a certain movie
for row in df.itertuples():
    ratings[row[1]-1, row[2]-1] = row[3]

#Using the below code, I confirm that 6.3% of the user-item ratings have a value
sparsity = float(len(ratings.nonzero()[0]))
sparsity /= (ratings.shape[0] * ratings.shape[1])
sparsity *= 100
print('Sparsity: {:4.2f}%'.format(sparsity))

##User-based Collaberative filtering
#Find item similarity
item_similarity = find_similarity(ratings)

#predict
pred = predict_topk(ratings, item_similarity, k=40)
pred = pd.DataFrame(pred)

# Load in movie data and get movie title
idx_to_movie = {}
with open('./data2/u.item', 'r', encoding = "ISO-8859-1") as f:
    for line in f.readlines():
        info = line.split('|')
        idx_to_movie[int(info[0])-1] = info[1]

#Using Pearson-R to find distances between items
item_correlation = 1 - pairwise_distances(ratings.T, metric='correlation')
item_correlation[np.isnan(item_correlation)] = 0.

#Find movies that similar uses like
idx = 1 # GoldenEye
movies = top_k_movies(item_correlation, idx_to_movie, idx)

#Based on user data, if a user likes the movie 'Golden Eye', then according to this model he also likes the following 5 movies:
print(movies)