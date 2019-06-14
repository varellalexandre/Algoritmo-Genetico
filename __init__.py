from geneticalgorithm import *

#função objetivo

def main(vector):
	x = 0
	for i in vector:
		x = x + i
	return x

#restrição 1
def restriction1(vector):
	return vector[0] >= 2

#restrição 2
def restriction2(vector):
	return vector[2] < 7

if __name__ == '__main__':
	aux = ga(main,[restriction1,restriction2],[[1,2,3,4],[5,6,7],[4,1,2]],tipo='max',len_populacao=4,workers=10)
	print(aux)