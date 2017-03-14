import math
import copy

def nearestNeighborClassifier(data, point, feature_subset, num_instances):
	""" 
	Computes distance to training points and
	returns the class label of the nearest training
	point.
	data: all the training points for this problem
	point: instance id of new data point that needs to be classified 
	num_instances: total instances in data set
	features: feature subset being used for classifier
	"""
	# Initialize variables for whole scope of function
	nearestNeighbor = 0
	shortest_distance = float('inf')

	# Loop over all instances
	for i in range(num_instances):
		# If the instance == the point, ignore/do nothing
		if point == i:
			pass
		# Else, find nearest neighbor and classify the point
		else:
			# nearestNeighbor keeps track of the nearest neighbor
			# shortest_distance determines which is nearest neighbor
			distance = 0
			# Get distance, compare and update nearestNeighbor
			# feature_subset: subset of features. ex) [1,2,4] -> features 1, 2 and 4
			for j in range(len(feature_subset)):
				distance = distance + pow((data[i][feature_subset[j]] - data[point][feature_subset[j]]), 2)

			distance = math.sqrt(distance)

			if distance < shortest_distance:
				nearestNeighbor = i 
				shortest_distance = distance

	return nearestNeighbor


def oneOutValidator(data, feature_subset, num_instances):
	"""
	Performs the one-out validation algorithm and returns the accuracy
	"""
	# FIX: Parameters may need to be changed depending on future fixes for algorithm

	# Loop i over all instances
	# set i to oneOut
	# Run nearest neighbor on oneOut
	# Check if the class of oneOut == class of nearest neighbor
	# Update accuracy
	correct = 0.0
	for i in range(num_instances):
		oneOut = i

		neighbor = nearestNeighborClassifier(data, oneOut, feature_subset, num_instances)

		if data[neighbor][0] == data[oneOut][0]:
			correct = correct + 1

	accuracy = (correct / num_instances) * 100

	return accuracy

def forwardSelection(data, num_instances, num_features):
	"""
	Returns the subset of features that has the highest accuracy
	by the forward selection algorithm.
	"""

	# Start with empty subset
	# use copy.deepcopy to update feature_subset
	feature_subset = []
	final_set = []
	# test each feature first, find highest accuracy and append to subset
	topAccuracy = 0.0

	# Loop a maximum of num_features times, 2^k - 1 possibilities
	for i in range(num_features):
		add_this = -1
		local_add = -1
		localAccuracy = 0.0
		for j in range(1, num_features + 1):
			if j not in feature_subset:
				# If the feature j is not in the subset, can perform algorithm. Otherwise, ignore.
				# Copy current subset into temp_subset
				temp_subset = copy.deepcopy(feature_subset)
				# Since j is not in the subset, we add it to temp and check accuracy
				temp_subset.append(j)

				accuracy = oneOutValidator(data, temp_subset, num_instances)
				print '\tUsing feature(s) ', temp_subset, ' accuracy is ', accuracy, '%'
				if accuracy > topAccuracy:
					topAccuracy = accuracy
					add_this = j
				if accuracy > localAccuracy:
					localAccuracy = accuracy
					local_add = j
		if add_this >= 0:
			feature_subset.append(add_this)
			final_set.append(add_this)
			print '\n\nFeature set ', feature_subset, ' was best, accuracy is ', topAccuracy, '%\n\n'
		else:
			print '\n\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)'
			feature_subset.append(local_add)
			print 'Feature set ', feature_subset, ' was best, accuracy is ', localAccuracy, '%\n\n'

	print 'Finished search!! The best feature subset is', final_set, ' which has an accuracy of accuracy: ', topAccuracy, '%'

def backwardElimination(data, num_instances, num_features, topAcc):
	"""
	Returns the subset of features that has the highest accuracy 
	by the backward elimination algorithm.
	"""

	# Similar to forward selection, except it works by elimination from a full set.
	# If j is in the set, then remove it from the temp set and test accuracy
	# If acc > highestAcc -> set new highestAcc and remove it from the actual subset
	# If at any time the accuracy is no longer increasing, break the loop
	# This is a greedy algorithm, so it will stop at a local maxima

	# Start with full feature set
	feature_subset = [i+1 for i in range(num_features)]
	final_set = [i+1 for i in range(num_features)]
	# Set current accuracy to accuracy found before feature algorithm
	topAccuracy = topAcc
	# Loop a maximum of num_features times, 2^k - 1 possibilties 
	for i in range(num_features):
		remove_this = -1
		local_remove = -1
		localAccuracy = 0.0
		for j in range(1, num_features + 1):

			if j in feature_subset:
				temp_subset = copy.deepcopy(feature_subset)

				temp_subset.remove(j)

				accuracy = oneOutValidator(data, temp_subset, num_instances)
				print '\tUsing feature(s) ', temp_subset, ' accuracy is ', accuracy, '%'
				if accuracy > topAccuracy:
					topAccuracy = accuracy
					remove_this = j
				if accuracy > localAccuracy:
					localAccuracy = accuracy
					local_remove = j
		if remove_this >= 0:
			feature_subset.remove(remove_this)
			final_set.remove(remove_this)
			print '\n\nFeature set ', feature_subset, ' was best, accuracy is ', topAccuracy, '%\n\n'
		else:
			print '\n\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)'
			feature_subset.remove(local_remove)
			print 'Feature set ', feature_subset, ' was best, accuracy is ', localAccuracy, '%\n\n'

	print 'Finished search!! The best feature subset is', final_set, ' which has an accuracy of accuracy: ', topAccuracy, '%'




def normalize(data, num_features, num_instances):
	"""
	Normalizes the data. X = (X - mean(X)) / std(X)
	Returns normalized instances.
	normalized[i][j] = (instances[i][j] - mean[j-1]) / std[j-1]; because instances[i][1] = feature 1 and mean[j-1] = feature 1
	"""

	# When using range(x to y)... starts from x stops at y - 1, so we need x to y + 1
	# Ex) num_features = 10, then range(1 to num_features + 1) -> 1 to 10

	# Get the mean for each feature, and store it in an array/list
	# Add feature X for all instances, divide by total # instances...
	mean = []
	for i in range(1, num_features + 1):
		mean.append((sum(row[i] for row in data)) / num_instances)

	# Get the std for each feature, and store it in an array/list
	# std formula -> (each point - mean)^2 / num_instances -> sqrt(variance)
	std = []
	for i in range(1, num_features + 1):
		variance = sum(pow((row[i] - mean[i-1]), 2) for row in data) / num_instances
		std.append(math.sqrt(variance))

	# Return data (just modified in original data array)
	for i in range(0, num_instances):
		for j in range(1, num_features + 1):
			data[i][j] = ((data[i][j] - mean[j-1]) / std[j-1])

	return data







def main():
	print 'Welcome to Ronson Lui\'s Feature Selection Algorithm.'
	file = raw_input('Type in the name of the file to test: ')

	# First column is the class, value always 1 or 2.
	# Other columns = features, maximum up to 64
	# 1 x x x x x x x x x ...
	# 2 x x x x x x x x x ...
	# Number of instances = total lines in file
	# Number features = total in one line - 1, bc first is classification
	# Max instances = 2048

	# Store data from file
	# Open file, error exception
	try:
		data = open(file, 'r')
	except:
		raise IOError('The file '+ file +' does not exist. Exiting program.')

	# Read in first line to see # features 
	firstLine = data.readline()

	num_features = len(firstLine.split()) - 1

	# Read in all lines on file to get # instances
	data.seek(0)
	num_instances = sum(1 for line in data)

	# Use seek(0) to reset cursor to start of file
	data.seek(0)

	# Store data into variable/array
	instances = [[] for i in range(num_instances)]
	for i in range(num_instances):
		instances[i] = [float(j) for j in data.readline().split()]

	# We now have a 2D array where instance[x][0] is the classification, and instance[x][num_features] is the last feature for x
	# x = instance id	
	
	# Algorithm selection
	print 'Type the number of the algorithm you want to run.'
	choice = int(raw_input())
	while choice < 1 or choice > 3:
		print 'Invalid choice, please try again.'
		choice = int(raw_input())

	print 'This dataset has ' + str(num_features) + ' features (not including the class attribute), with ' + str(num_instances) + ' instances.'

	# CONVERT/NORMALIZE DATA -> begin search
	print 'Please wait while I normalize the data... Done!'
	normalized_instances = normalize(instances, num_features, num_instances)

	# Run nearest neighbor + one out validation + ALL features, print results
	all_features = []
	for i in range(1, num_features + 1):
		all_features.append(i)

	accuracy = oneOutValidator(normalized_instances, all_features, num_instances)
	print 'Running nearest neighbor with all ', num_features, ' features, using "leaving-one-out" evaluation, I get an accuracy of ', accuracy, '%.'

	# TO FIX: Add algorithm to make the subsets in the chosen algorithms


	# TO-DO: BE methods, choice redirection
	print 'Beginning search.\n\n'

	if choice == 1:
		forwardSelection(normalized_instances, num_instances, num_features)
	elif choice == 2:
		backwardElimination(normalized_instances, num_instances, num_features, accuracy)
	elif choice == 3:
		print 'Special algorithm not completed yet, exiting.'


















if __name__ == '__main__':
	main()
