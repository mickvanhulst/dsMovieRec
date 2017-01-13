#Import models
from KNN import main_knn 
from collab_user_filtering import main_cuf

from collections import Counter
import sys
import pandas as pd
import sqlalchemy

def main(user):
    # Init result and add results of models
    result = []
    result.extend(main_cuf(user))
    result.extend(main_knn(user))
    
    # Count occurences
    recommendations = Counter(result)

    # Get first 30 results
    top_results = sorted(recommendations, key=recommendations.get)[:30]

    # Create dataframe and insert into database
    recom_dict = {user: top_results}

    recommendations = pd.DataFrame.from_dict(({"userId": user, "movieId": recom_dict[user]}))

    # Create engine
    engine = sqlalchemy.create_engine('mysql+pymysql://dsMinor:dsMinor!123@81.204.145.155/MoviesDS?charset=utf8',
                                      encoding="utf-8")

    # Save recommendations in db
    recommendations.to_sql(con=engine, name='userRecommendations', if_exists='append', index=False)

if __name__ == '__main__':
    user = int(sys.argv[1])
    main(user)