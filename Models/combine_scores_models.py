#Import models
from KNN import main_knn 
from collab_user_filtering import main_cuf

from collections import Counter

def main():
    # Setup connection
    #conn = pymysql.connect(host='81.204.145.155', user="dsMinor", passwd="dsMinor!123", db='MoviesDS', 
    #    charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    # Models
    result = []
    result.extend(main_cuf(user))
    result.extend(main_knn(user))
    
    recommendations = Counter(result)

    # Count results using dictCounter
    # count = Counter(results_count)

    # Get first 30 results
    top_results = sorted(recommendations, key=recommendations.get)[:30]
    
    # Save recommendations in table for user

    return top_results

if __name__ == '__main__':
    user = 670
    data = main(user)
    print(data)



