from Instance import Instance
import math

def nearestNeighborClassifier(data, point):
	""" 
	Computes distance to training points and
	returns the class label of the nearest training
	point.
	data: all the training points for this problem
	point: the new data point that needs to be classified 
	"""


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

















if __name__ == '__main__':
	main()
