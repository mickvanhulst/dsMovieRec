import pandas as pd
import re
import operator
import pymysql
import sqlalchemy
from collections import Counter

def get_highest_occurrence(selected_genre_occurrence):
    highest_occurring_genre = [max(selected_genre_occurrence, key=selected_genre_occurrence.get)]
    top_genre_occurrence = selected_genre_occurrence[highest_occurring_genre[0]]

    for genre, occurrence in selected_genre_occurrence.items():
        if occurrence == top_genre_occurrence:
            if genre not in highest_occurring_genre:
                highest_occurring_genre.append(genre)
    return highest_occurring_genre


def entries_to_remove(entries, the_dict):
    for key in entries:
           if key in the_dict:
                del the_dict[key]

def main(userId):
    # Setup connection
    conn = pymysql.connect(host='81.204.145.155', user="dsMinor", passwd="dsMinor!123", db='MoviesDS', 
        charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    engine = sqlalchemy.create_engine('mysql+pymysql://dsMinor:dsMinor!123@81.204.145.155/MoviesDS?charset=utf8', encoding="utf-8")

    # Select movies where at least one rating and rating higher than 3
    movies = pd.read_sql("""select m.movieId as movieId, genres 
                            from movies m
                            inner join (select movieId, count(*) 
                                from ratings  
                                where rating > 3
                                group by movieId
                                having count(*) > 0)
                            AS cnt ON cnt.movieId = m.movieId""", con=conn)

    userRatings = pd.read_sql('select * from ratings where userId = ' + str(userId) + ' and rating > 3', con=conn)
    number_of_recommendations = 10

    movies_dict = movies.set_index('movieId')['genres'].to_dict()
    rated_genres = []

    for movieId in userRatings['movieId']:
        rated_genres.extend(movies_dict[movieId].split("|"))

    rated_genre_occurrence = Counter(rated_genres)

    top1_genres = get_highest_occurrence(rated_genre_occurrence)

    entries_to_remove(top1_genres, rated_genre_occurrence)
    top2_genres = get_highest_occurrence(rated_genre_occurrence)

    entries_to_remove(top2_genres, rated_genre_occurrence)
    top3_genres = get_highest_occurrence(rated_genre_occurrence)

    entries_to_remove(top3_genres, rated_genre_occurrence)
    low_rated_genres = rated_genre_occurrence

    movies_recommendation_rating = {}
    
    top1_genre_perc = 50 / (len(top1_genres) if len(top1_genres) > 0  else 1)
    top2_genre_perc = 25 / (len(top2_genres) if len(top2_genres)  > 0 else 1)
    top3_genre_perc = 20 / (len(top3_genres) if len(top3_genres) > 0 else 1)
    low_rated_genre_perc = 5 / (len(low_rated_genres) if len(low_rated_genres) > 0 else 1)

    for movie_id, movie_genres in movies_dict.items():

        movie_recommendation_rating = 0

        for genre in top1_genres:
            if genre in movie_genres:
                movie_recommendation_rating += top1_genre_perc

        for genre in top2_genres:
            if genre in movie_genres:
                movie_recommendation_rating += top2_genre_perc

        for genre in top3_genres:
            if genre in movie_genres:
                movie_recommendation_rating += top3_genre_perc

        for genre in low_rated_genres:
            if genre in movie_genres:
                movie_recommendation_rating += low_rated_genre_perc

        movies_recommendation_rating[movie_id] = movie_recommendation_rating

    
    recommended_movies = dict(sorted(movies_recommendation_rating.items(), 
        key=operator.itemgetter(1), reverse=True)[:number_of_recommendations])
    
    recommended_movies = list(recommended_movies.keys())

    return recommended_movies
    #return 1

if __name__ == '__main__':
    # Get userId from PHP
    #userId = sys.argv[1]
    userId = 669
    data = main(userId) # userId meegeven
    print(data)