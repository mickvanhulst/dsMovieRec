# Import packages
import pandas as pd
import numpy as np
import pymysql
from datetime import date
import sqlalchemy

def get_rand_movies(amount_to_gen, movies, ratings, conn):
	# Filter movies/ratings where movie max 10 years old.
	movies_max_years_old = movies[movies['year'] <= (date.today().year - 10)]
	ratings = ratings[ratings['movieId'].isin(list(movies_max_years_old['movieId'].values))]

	# Calculate average scores/total reviews recieved for each movie.
	# More ratings > more people know the movie > higher chance that the user knows the movie
	agg_movie = ratings.groupby(['movieId'])['rating'].agg(['mean', 'count'])

	# Calculate total average/average count of all movies.
	ratings_avg = ratings['rating'].mean()
	ratings_avg_cnt = agg_movie['count'].mean()


	# If movie avg & count is higher than total avg & count.
	mov_filtered = agg_movie[(agg_movie['mean'] >= ratings_avg) & (agg_movie['count'] >= ratings_avg_cnt)]

	# generate fifty random movies and save movieId's in list
	rand_sample = list(mov_filtered.sample(amount_to_gen).index)
	print(rand_sample)
	# Save to db
	save_sample_db(rand_sample, conn)
	
	return (rand_sample)

def save_sample_db(rand_sample, conn):
	# Create dataframe from rand_sample and add points
	rand_sample = pd.DataFrame(rand_sample)
	rand_sample['points'] = 30
	rand_sample.columns = ['movieId', 'points']

	# Create engine
	engine = sqlalchemy.create_engine('mysql+pymysql://dsMinor:dsMinor!123@81.204.145.155/MoviesDS?charset=utf8', encoding="utf-8")
	
	# Save the movies in db 
	rand_sample.to_sql(con=engine, name='sampleUserInitial', if_exists='append', index=False)

	# Use a count system. Every movie starts with 30 points.
	# If user rates the movie with a high score then add a count.
	# If user rates it low, then substract a point.
	# If user does not know the movie substract two counts.
	# If movie points are lower or equal to zero, remove the movie and 
	# adds a new movie by running this program.

def check_amount_gen(conn, MINIMUM_TOTAL):
	# Check total amount of rows with points higher than 0.
	count_sample = pd.read_sql("select count(*) from sampleUserInitial where points > 0", con=conn)

	# Substract result from the required total in our table.
	count_sample = MINIMUM_TOTAL - count_sample.iat[0,0]
	
	return count_sample

def main():
	# Setup connection
	conn = pymysql.connect(host='81.204.145.155', user="dsMinor", passwd="dsMinor!123", db='MoviesDS', 
		charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

	# Minimum total (static variable)
	MINIMUM_TOTAL = 50

	# Check how many movies need to be generated
	amount_to_gen = check_amount_gen(conn, MINIMUM_TOTAL)
	print(amount_to_gen)
	
	if(amount_to_gen > 0):
		#Get movies & ratings
		movies = pd.read_sql("select * from movies", con=conn)
		ratings = pd.read_sql("select * from ratings", con=conn)

		return (get_rand_movies(amount_to_gen, movies,ratings, conn))
	else:
		return 'No rows generated'

if __name__ == '__main__':
    data = main()
    print(data)

## Get init recommendation scores, then use those scores for the content-based algo.

# note: Eventueel meerdere movies selecteren (dus 5 dichtste bij) dan op basis van user input steeds meer films genereren.
# User vindt film één leuk maar niet film twee. Skip films die lijken op film twee qua genre and ga verde rop deel één.
# Niet vergeten om dan alsnog een stukje random toe te voegen. <--- Hierbij zou content based echt perfect zijn.
# Waarom content based over user based? Omdat we op dat moment nog niet genoeg informatie over de user hebben verzameld
# waarop we aanbevelingen kunnen maken op een user-based niveau.


# Matrix maken van keywords en dan alle keywords eruitfilteren welke minder dan 2 keer voorkomen en degene die meer dan het gemiddelde voorkomen
# Door de veelvoorkomende keywords eruit te halen, filter je woorden welke eigenlijk niet veel toevoegen aan het al gebruikte genre.
# Als een keyword 'Avontuur' bevat en het genre is al 'avontuur' boeit het natuurlijk niks. Plus het zorgt ervoor dat je alsnog 
# heel globaal blijft zoeken. Door keywords te pakken welke minder voorkomen (denk aan '007'), zoek je al specifieker.