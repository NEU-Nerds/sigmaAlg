import _pickle as pickle
import os
import shutil
import time
import sys
# import json

# from objsize import get_deep_size

def sigmaBatches(s, batchSize):
	batch = []
	for p in partitions(s):
		# print(f"pre p: {p}")
		p.sort()
		p.reverse()
		# print(f"sorted p: {p}")
		p = tuple(p)
		# pc = getConjugate(p)
		# if pc != p:
		# 	batch.append(pc)
		batch.append(p)

		if len(batch) >= batchSize:
			yield batch
			batch = []
	yield batch

#http://code.activestate.com/recipes/218332-generator-for-integer-partitions/
def partitions(n):
	# base case of recursion: zero is the sum of the empty list
	if n == 0:
		yield []
		return

	# modify partitions of n-1 to form partitions of n
	for p in partitions(n-1):
		yield [1] + p
		if p and (len(p) < 2 or p[1] > p[0]):
			yield [p[0] + 1] + p[1:]

#from sympy - thanks!
#https://github.com/sympy/sympy/blob/master/sympy/combinatorics/partitions.py
def getConjugate(node):
	j = 1
	temp_arr = list(node) + [0]
	k = temp_arr[0]
	b = [0]*k
	while k > 0:
		while k > temp_arr[j]:
			b[k - 1] = j
			k -= 1
		j += 1
	return tuple(b)

def getChildren(node):
	node = list(node)
	for i in range(len(node)):
		if i != 0:
			yield tuple(node[:i])
		for j in range(1, node[i]):
			# if i == 0 and j == 0:
			# 	continue
			#"biting" at i,j
			ret = node[:]
			nI = i
			while nI < len(node) and node[nI] > j:
				ret[nI] = j
				nI += 1
			yield tuple(ret)

# pass in a path representing a node.
# returns a list of bools with the same length
# the bool at each index represents whether the int at the index - 1 and the index are the same
# index 0 is always false
def layerEquivalence(path):
		layerEq = [False] * len(path)
		for i in range(1, len(path)):
			layerEq[i] = path[i] == path[i-1]
		return layerEq

def emptyDir(folder):
	for filename in os.listdir(folder):
		file_path = os.path.join(folder, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))




# def evensLoad(x):
# 	return load(x)
#
# def rootsLoad(x):
# 	return load(x)

def startSigma():
	files = os.listdir(f"./evens/")
	max = 0
	for file in files:
		s = file[len("evens_"):]
		s = s[:-len(".dat")]
		# print(s)
		try:
			if (int(s) > max):
				max = int(s)
		except:
			pass

	# print(files)
	print(max)
	return max

def load(fileName):
	with open (fileName, 'rb') as f:
		return pickle.load(f)

# def rootsStore(x1, x2):
# 	store(x1, x2)

def store(data, fileName):
	with open(fileName, 'wb') as f:
		pickle.dump(data, f)
"""
def load(fileName, isSet=True):
	with open(fileName, "r") as file:
		jData = file.read()
		# +" "
		# jData = "[" + jData[1:-1]
		data = json.loads(jData)
		try:
			if isSet:
				data = set(data)
		except:
			print(f"data: {data}\tfileName: {fileName}")

			exit()
		return data

def store(data, fileName):
	with open(fileName, "w") as file:
		jData = json.dumps(list(data))
		file.write(jData)
		# file.write(str(data))
		# return 1
"""
