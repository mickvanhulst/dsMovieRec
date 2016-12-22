import pandas as pd
import math
import numpy as np
import operator
 
# Turn off annoying warning (Link: http://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas)
pd.options.mode.chained_assignment = None

def calc_euclidean(train_data, test_data, train_point, test_point, features):
	total_dist = 0

	for feature in features:

		dist = math.pow(test_data.loc[test_point, feature] - train_data.loc[train_point, feature], 2)
		total_dist += dist

	# d = sqrt((a1-b1)^2 + (a2-b2)^2 + (a3-b3)^2 + (a4-b4)^2)
	return math.sqrt(total_dist)

def det_nearest_neighbors(train_data, test_data, test_point, features, k):
	# Loop through all and calculate euclidean distance
	dist_dict = {}

	for train_point in train_data.index:
		# Set index of training point plus euclidean distance
		dist_dict[train_point] = calc_euclidean(train_data, test_data, train_point, test_point, features)

	# Get k highest values
	dict_top_k = sorted(dist_dict, key=dist_dict.get, reverse=True)[:k]

	return dict_top_k


def KNN(test_data, train_data, features, target_col_name, k):
	for test_point in test_data.index:
		# Find k number of nearest neighbors
		nearest_neighbors = det_nearest_neighbors(train_data, test_data, test_point, features, k)

		# Convert indexes to classes
		nearest_neighbors = train_data[train_data.index.isin(nearest_neighbors)]

		# Count, grouped by class
		agg_class = nearest_neighbors.groupby(target_col_name).size()
		
		# Max count is new class
		test_data.loc[test_point, 'classify'] = agg_class.idxmax()
	
	# determine accuracy
	len_classify_equals_target = len(test_data[test_data[target_col_name] == test_data['classify']].index) 
	len_test_data = len(test_data.index)
	accuracy = len_classify_equals_target / len_test_data
				
	return test_data, accuracy


# Get n neighbors that are closest with current ratings of current user, so compare only users that 
# rated the same movies as other user. This results a set of users. Then get the remaining 
# movies of the neighbored user, and give those as the result.