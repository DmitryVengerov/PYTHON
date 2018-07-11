def const(b):
	return (b-4) ** 2

def num_slope(b):
	h = 0.0001
	return (const(b+h) - const(b))/h

def slope(b):
	return 2 * (b - 4) 


b = -20 
b = b - .1 * slope(b)

for i in range(30):
	b = b - .1 * slope(b)
	print(b)
print(slope(b))
