import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
import random
import math
from ggplot import *

def det_neighbours(data, x, epsilon, min_density, features):
	# Determine core points using the euclidean distance
	# d = sqrt((a1-b1)^2 + (a2-b2)^2 + (a3-b3)^2 + (a4-b4)^2)
	neighbour_list = []
	for y in data.index:
		total_dist = 0
		for feature in features:
			dist = math.pow(data.loc[x, feature] - data.loc[y, feature], 2)
			total_dist += dist
			
		if(math.sqrt(total_dist) >= epsilon):
			# If within range, append index to list
			neighbour_list.append(y)
	return neighbour_list

def cluster_expansion(data, epsilon, min_density, features, cluster, neighbour_list):
	# Loop through neighbors
	print(data[data.index.isin(neighbour_list)].index)
	for z in data[data.index.isin(neighbour_list)].index:
		#print(z)
		# Unvisited or marked as noise
		if(data.loc[z, 'visited'] == False):
			# Mark as visited
			data.loc[z, 'visited'] == True
			neighbours_z = det_neighbours(data, z, epsilon, min_density, features)
			
			if(len(neighbours_z) >= min_density):
				neighbour_list.extend(neighbours_z)

		else:
			data.loc[z, 'cluster'] == cluster
	
	# Assign neighbours to same cluster
	data.loc[data.index.isin(neighbour_list), 'cluster'] = cluster

	return data
	
def dbscan(data, epsilon, min_density, features):
	cluster = 0
	for x in data.index:
		print(x)
		# Mark p as visited
		data.loc[x, 'visited'] = True

		# Get neighbor list
		neighbour_list = det_neighbours(data, x, epsilon, min_density, features)

		# If neighbour count higher than minimal density, apply cluster.
		if(len(neighbour_list) >= min_density):
			data.loc[x, 'cluster'] = cluster

			# Start cluster expansion for each point which is in neighboorhood
			data = cluster_expansion(data, epsilon, min_density, features, cluster, neighbour_list)
		
		# Cluster expansion done, start new cluster.
		cluster += 1
	
	return data

def main():
	#load iris dataset. Class -> target, which consists of three values (0,1,2)
	iris = load_iris()
	data = pd.DataFrame(data=np.c_[iris['data'], iris['target']],
	                     columns=iris['feature_names'] + ['target'])
	
	# add new column cluster and determine features
	data['cluster'] = np.nan
	data['visited'] = False
	features = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
		
	# init max distance and minimal density.
	epsilon = 5.5
	min_density = 5 

	data = dbscan(data, epsilon, min_density, features)

	print(ggplot(data, aes(x='sepal length (cm)', y='sepal width (cm)', color='cluster')) + \
  				geom_point(colour='steelblue'))

if __name__ == '__main__':
    main()


# Clusters genereren.
# Get cluster waar user inzit.
# Get all movies van users uit andere clusters.
# Kijk welke huidige user niet heeft gezien.
# Niet gezien = recommendation