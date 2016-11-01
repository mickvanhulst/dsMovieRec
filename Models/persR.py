import pandas as pd

#Load data
r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
ratings = pd.read_csv('../data/ratings.csv', sep='\t', names=r_cols,
 encoding='latin-1')

from scikits.crab.models import MatrixPreferenceModel
model = MatrixPreferenceModel()

from scikits.crabs.metric import pearson_correlation
from scikits.crab.similarities import UserSimilarity

#Build similarity
similarity = UserSimilarity(model, pearson_correlation)

from crab.recommenders.knn import UserBasedRecommender

recommender = UserBasedRecommender(model, similarity, with_preference=True)
recommender.recommend(5)