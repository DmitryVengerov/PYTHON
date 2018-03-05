

hexa_list = [[0,1,1,0,1],[1,1,1,0,1],[1,0,1,0,1],[0,0,0,0,1],[0,1,0,1,1]]
	

def findcenter(array):
	
	acc = 0
	centerHexa = len(array)//2
	return centerHexa

def find_n(array, x, y):
	acc = 0
	if array[x - 2][y] == 1:
		acc == acc + 1
	if array[x-1][y-1] == 1:
		acc == acc + 1
	if array[x+1][y-1] == 1:
		acc == acc + 1
	if array[x-1][y+1] == 1:
		acc == acc + 1
	if array[x+1][y+1] == 1:
		acc == acc + 1	
	if array[x + 2][y] == 1:
		acc == acc + 1
	print(acc)
	return acc


def cell_life(array):
	acc = 0
	coordinates = findcenter(array)
	for i in range(len(array)):
		for j in range(len(array[i])):
				if array[i][j] == 1:
					#print('Pos x', i, 'Pos y', j)
					acc = acc +1
	print("Number of live ",acc)				
	#keepALive(acc)	

def finder_neg(array,posX,posY):
	for i in range (posX,posY):
		print(array[i])
		


#def findAr(array,posX, posY):

def keepALive(acc):
	if acc < 2 or acc > 3 :print("cell is dead")
	else:print("cell is alive")


def test(array, temp_center ):
	fact_center = findcenter(array)
	if int(temp_center) == findcenter: print("test sec")
	else: print("test fail")


#generate(hexa_list)
#findcenter(hexa_list)
#test(hexa_list, 2)
cell_life(hexa_list)
finder_neg(hexa_list, 0,4)
#find_n(hexa_list,2,1)
#findAr()