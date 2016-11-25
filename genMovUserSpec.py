#Import packages
import pandas as pd # mov processing, CSV file I/O (e.g. pd.read_csv)
import pymysql

Connection = pymysql.connect(host='81.204.145.155', user="dsMinor", passwd="dsMinor!123", db='MoviesDS', 
	charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

movies = pd.read_sql("select * from movies", con=Connection)
ratings = pd.read_sql("select * from ratings", con=Connection)


# Calculate total average of all movies and total amount of genres.
ratings_avg = ratings['rating'].mean()

# Calculate average scores/total reviews recieved for each movie
ratings_total = ratings.groupby('movieId')['rating'].count()
ratings_total.columns = ['movieId', 'Count']

ratings_avg_movie = ratings.groupby(['movieId'])['rating'].mean()
ratings_avg_movie.columns = ['movieId', 'avg']

# Keep movies that have an average rating that is at least higher than the average of all movies.
mov_high_then_avg = ratings_avg_movie[ratings_avg_movie.values >= ratings_avg]

# Merge datasets
mov_merg = pd.merge(mov_high_then_avg.to_frame(), ratings_total.to_frame(), left_index=True, right_index=True, how='left')
mov_merg.columns = ['avg', 'cnt']
print(mov_merg)

# Recalculate first, second and third quantiles for ratings (filtered dataset).
firstQ = 0
secondQ = 0
thirdQ = 0

# For each genre get firstQ/secondQ/thirdQ movies where the count is the highest (more ratings is more thrustworthy).
# Where it is closest to the quartiles.


# note: Eventueel meerdere movies selecteren (dus 5 dichtste bij) dan op basis van user input steeds meer films genereren.
# User vindt film één leuk maar niet film twee. Skip films die lijken op film twee qua genre and ga verde rop deel één.
# Niet vergeten om dan alsnog een stukje random toe te voegen. <--- Hierbij zou content based echt perfect zijn.
# Waarom content based over user based? Omdat we op dat moment nog niet genoeg informatie over de user hebben verzameld
# waarop we aanbevelingen kunnen maken op een user-based niveau.


# Matrix maken van keywords en dan alle keywords eruitfilteren welke minder dan 2 keer voorkomen en degene die meer dan het gemiddelde voorkomen
# Door de veelvoorkomende keywords eruit te halen, filter je woorden welke eigenlijk niet veel toevoegen aan het al gebruikte genre.
# Als een keyword 'Avontuur' bevat en het genre is al 'avontuur' boeit het natuurlijk niks. Plus het zorgt ervoor dat je alsnog 
# heel globaal blijft zoeken. Door keywords te pakken welke minder voorkomen (denk aan '007'), zoek je al specifieker.

