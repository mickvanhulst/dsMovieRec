import pandas as pd
import graphlab
graphlab.product_key.set_product_key('BCB5-EC60-E065-BABC-FEDA-EA99-7F2E-15CD')

# pass in column names for each CSV and read them using pandas. 
# Column names available in the readme file

#Reading users file:
u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv('../data2/u.user', sep='|', names=u_cols,
 encoding='latin-1')

#Reading ratings file:
r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
ratings = pd.read_csv('../data2/u.data', sep='\t', names=r_cols,
 encoding='latin-1')

#Reading items file:
i_cols = ['movie id', 'movie title' ,'release date','video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
items = pd.read_csv('../data2/u.item', sep='|', names=i_cols,
 encoding='latin-1')

#Pre-divided training/test dataset
r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
ratings_base = pd.read_csv('../data2/ua.base', sep='\t', names=r_cols, encoding='latin-1')
ratings_test = pd.read_csv('../data2/ua.test', sep='\t', names=r_cols, encoding='latin-1')

#Create SFrames since we'll be  using GraphLab
train_data = graphlab.SFrame(ratings_base)
test_data = graphlab.SFrame(ratings_test)

##Popularity model
popularity_model = graphlab.popularity_recommender.create(train_data, user_id='user_id', item_id='movie_id', target='rating')

#Get recommendations for first 5 users and print them
#users = range(1,6) specifies user ID of first 5 users
#k=5 specifies top 5 recommendations to be given
popularity_recomm = popularity_model.recommend(users=range(1,6),k=5)
#popularity_recomm.print_rows(num_rows=25)

ratings_base.groupby(by='movie_id')['rating'].mean().sort_values(ascending=False).head(20)

##Collaberative filtering model
#Train Model
item_sim_model = graphlab.item_similarity_recommender.create(train_data, user_id='user_id', item_id='movie_id', target='rating', similarity_type='pearson')

#Make Recommendations:
item_sim_recomm = item_sim_model.recommend(users=range(1,6),k=5)
item_sim_recomm.print_rows(num_rows=25)

##Compare model performance
#model_performance = graphlab.compare(test_data, [popularity_model, item_sim_model])
#graphlab.show_comparison(model_performance,[popularity_model, item_sim_model])