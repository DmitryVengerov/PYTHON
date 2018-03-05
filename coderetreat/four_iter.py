cell_list = [[0,0,0,0,0],[0,1,1,1,0],[0,0,1,0,0],[0,1,1,1,0],[0,0,0,0,0]]


# temp = [[1,3],[2,2]]


def generate(array):
	for i in range(len(array)):
		for j in range(len(array[i])):
			print(array[i][j])
	

def center(array):

	width = len(array)
	centerPos = width // 2 
	
	return centerPos

def neighbours(array):
	acc = -1
	tempArray = []
	centerPos = center(array)
	
	for i in range(centerPos-1,centerPos+2):
		for j in range(1,4):
		#print(array[i][j])
			if( array[i][j] == 1):
				acc = acc + 1
				
				print(i,j)

			
	#print(tempArray)
	print("У клетки'", centerPos,centerPos,"'",acc, "соседей")
	print("Клетка должна погибнуть")		

def test(array):

	test_center = center(array)
	arr_center = 2;

	if( arr_center == test_center):
		"Test sec"
	else:
		"Test Failed"



#generate(cell_list)
neighbours(cell_list)
test(cell_list)
