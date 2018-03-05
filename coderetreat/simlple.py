generatedList = [[0,0,0],[0,1,0],[0,0,0]]

def generate(array):
	for i in range(len(generatedList)):
		print("\n")
		for j in range(len(generatedList[i])):
			print(generatedList[i][j])
		

def find(array):
	acc = 0
	for i in range(len(generatedList)):
		for j in range(len(generatedList[i])):
			if generatedList[i][j] == 1:
				acc = acc + 1
				print("кол-во живых",acc)
				if acc > 1:
					print("есть соседи")
				else:
					print("нет соседей")

def findSosedy(array, posX, posY):
	acc = 0
	for i in range(posX - 1, posX + 2):
		for j in range(posY -1, posY + 2):
			if array[i][j] == 1:
				acc = acc + 1
	acc = acc - 1
	# print("Кол-во соседей ",acc, "у клетки с координатами", posX, " ",posY)
	return acc
	
def good(array):
	acc = 0
	for i in range(len(array)):
		for j in range(len(array[i])): 
			if array[i][j] == 1:
				sosedy = findSosedy(array,i,j)
				if sosedy > 3 or sosedy < 2 :
					print("Cell is dead")
					
				else:
					print("Cell is life")


def test(array, posX, posY, result):
	f = findSosedy(array, posX,posY)
	temp = result
	if f == temp: 
		print("Test successful")
	else:
		print("Test Failed")
	


generate(generatedList)
# find(generatedList)
findSosedy(generatedList, 1, 1)
good(generatedList)
#test(generatedList, 1, 1, 6)
