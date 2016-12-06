import pandas as pd
import re
import operator

number_of_recommendations = 10
movies = pd.read_csv('/Users/yoerivanbruchem/Dropbox/DATA/Bilal & Yoeri/data/movie_metadata.csv')

userRatings = {'tt1229340': 3, 'tt0120903': 2, 'tt1405365': 3, 'tt0385056': 4,
               'tt0105112': 4, 'tt0407887': 5, 'tt0480251': 4, 'tt0068699': 4,
               'tt0799934': 4}


def get_movie_id_from_url(url):
    movie_id = re.sub("/\?ref_=fn_tt_tt_1", "", url)
    movie_id = re.sub("http://www.imdb.com/title/", "", movie_id)
    return movie_id

movies['movie_imdb_link'] = movies['movie_imdb_link'].apply(get_movie_id_from_url)
movies.rename(columns={'movie_imdb_link': 'imdb_id'}, inplace=True)

movies_dict = movies.set_index('imdb_id')['genres'].to_dict()

userRatings_genres = []
userRatings = dict((k, v) for k, v in userRatings.items() if v >= 3)

for movie_id, rating in userRatings.items():
    userRatings_genres = userRatings_genres + movies_dict[movie_id].split("|")

rated_genres = list(set(userRatings_genres))
rated_genre_occurrence = {}

for single_genre in rated_genres:
    genre_occurrence = 0
    for genre in userRatings_genres:
        if genre == single_genre:
            genre_occurrence += 1
    rated_genre_occurrence[single_genre] = genre_occurrence

sum_total_ratings = sum(rated_genre_occurrence.values())

# Get top genres


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

top1_genres = get_highest_occurrence(rated_genre_occurrence)

entries_to_remove(top1_genres, rated_genre_occurrence)
top2_genres = get_highest_occurrence(rated_genre_occurrence)

entries_to_remove(top2_genres, rated_genre_occurrence)
top3_genres = get_highest_occurrence(rated_genre_occurrence)

entries_to_remove(top3_genres, rated_genre_occurrence)
low_rated_genres = rated_genre_occurrence

movies_recommendation_rating = {}

top1_genre_perc = 50/len(top1_genres)
top2_genre_perc = 25/len(top2_genres)
top3_genre_perc = 20/len(top3_genres)
low_rated_genre_perc = 5/len(low_rated_genres)

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

recommended_movies = dict(sorted(movies_recommendation_rating.items(), key=operator.itemgetter(1), reverse=True)
                          [:number_of_recommendations])

print(recommended_movies)





