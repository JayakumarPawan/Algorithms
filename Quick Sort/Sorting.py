
def insertionSort(list, start, end):
	for i in range(start,end+1):
		toInsert = list[i]
		j = i-1
		while j>=0 and toInsert < list[j]:
			list[j+1] = list[j]
			j-=1
		list[j+1] = toInsert
	return list
		
def partition(list, start, end):
	i =start
	pivot = list[end]
	for j in range(start,end):
		if(list[j] <= pivot):
			temp = list[i]
			list[i] = list[j]
			list[j] = temp
			i+=1
	list[end] = list[i]
	list[i] = pivot
	return i, list


def quickSort(list, start, end, minSize):
	if end-start <= minSize:
		return insertionSort(list,start,end)
		
	pivot, list = partition(list, start, end)
	list = quickSort(list, start, pivot-1, minSize)
	list = quickSort(list, pivot+1, end, minSize)
	return list
