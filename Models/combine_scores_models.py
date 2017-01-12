def main():
    # Setup connection
    conn = pymysql.connect(host='81.204.145.155', user="dsMinor", passwd="dsMinor!123", db='MoviesDS', 
        charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    # Models
    models = ['KNN', 'collab']
    result = []

    for model in models:
        # Get all results from models
        print('a')
        # result.extend(model_result) <-- all result for count

    # Count results using dictCounter
    # count = Counter(results_count)

    # Get first 30 results

    # Save recommendations in table for user

    return recommendations

if __name__ == '__main__':
    data = main()
    print(data)



