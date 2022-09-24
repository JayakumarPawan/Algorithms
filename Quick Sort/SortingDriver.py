
from Sorting import insertionSort, quickSort
import copy
import random
import time
import sys

def checkSorted(orig, sorted):

	# Make sure size is the same
	if len(orig) != len(sorted):
		print("ERROR...original list and sorted list have different lengths...",end='')
		return False
	
	# Make sure new array is sorted
	for i in range(1,len(sorted)):
		if sorted[i] < sorted[i-1]:
			print("ERROR...the sorted list does not appear to be correctly sorted...",end='')
			return False

	# Make sure the same elements are in each array
	count = {}
	for i in range(len(orig)):
		if orig[i] not in count:
			count[orig[i]] = 1
		else:
			count[orig[i]] = count[orig[i]]+1
		
		if sorted[i] not in count:
			count[sorted[i]] = -1
		else:
			count[sorted[i]] = count[sorted[i]]-1;

	for key in count:
		if count[key] != 0:
			print("ERROR...The sorted list does not contain the same elements that the original list does...",end='')
			return False
	
	return True


sys.setrecursionlimit(100000)
SIZE = 100000
	
# Make an array (vector) to sort. Fill with random numbers
list = []
for i in range(SIZE):
	list.append((int)(random.randrange(SIZE)))

# Make copies to sort
ins = copy.deepcopy(list) 
qui = copy.deepcopy(list)
ctrl = copy.deepcopy(list)
print("Sorting using insertion sort...",end='')
t1 = time.time()
#insertionSort(ins, 0, len(list)-1);
insertTime = time.time()-t1
print("DONE\nChecking if sorted correctly...",end='')

checkSorted(list, ins);

print("DONE")

print("Sorting using quick sort...",end='')
t1 = time.time()
quickSort(qui, 0, len(list)-1, 30);
quickTime = time.time() - t1
print("DONE\nChecking if sorted correctly...",end='')
checkSorted(list, qui);
print("DONE")

t1 = time.time()
ctrl.sort()
ctrlTime = time.time() - t1
print('number of elements:', SIZE)
print('time taken for insertion sort: ', insertTime)
print('time taken for quick sort: ', quickTime)
print('time taken for built in: ', ctrlTime)


