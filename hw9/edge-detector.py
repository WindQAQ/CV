import argparse
from math import sqrt
from itertools import product
from PIL import Image

BLACK, WHITE = 0, 255

sumTuple = lambda a, b: (a[0]+b[0], a[1]+b[1])

edge = lambda x, T: (WHITE if x < T else BLACK)

def flip(p, bound):
	if p < 0:
		return -p
	elif p >= bound:
		return 2 * bound - 1 - p

	return p

def convolve(M, size, pos, mask):
	ret = 0;
	X, Y = int(len(mask)/2), int(len(mask[0])/2)
	for (i, row) in enumerate(mask):
		for (j, value) in enumerate(row):
			offset = (i-X, j-Y)
			(x, y) = sumTuple(pos, offset)
			x = flip(x, size[0])
			y = flip(y, size[1])
			ret += M[x, y] * value
	
	return ret

def edge_detect(pix, size, mask, thres, type):
	if type == 'sum':
		return {p: edge(sqrt(sum( \
					[convolve(pix, size, p, m)**2 for m in mask])), thres) \
						for p in product(range(size[0]), range(size[1]))}
	elif type == 'max':
		return {p: edge(max( \
					[convolve(pix, size, p, m) for m in mask]), thres) \
						for p in product(range(size[0]), range(size[1]))}

def Roberts(pix, size, thres):
	mask = [[ [-1, 0], [0, 1] ], \
			[ [0, -1], [1, 0] ]]

	return edge_detect(pix, size, mask, thres, 'sum')

def	Prewitt(pix, size, thres):
	mask = [[ [-1, -1, -1], [0, 0, 0], [1, 1, 1] ], \
			[ [-1, 0, 1], [-1, 0, 1], [-1, 0, 1] ]]

	return edge_detect(pix, size, mask, thres, 'sum')

def	Sobel(pix, size, thres):
	mask = [[ [-1, -2, -1], [0, 0, 0], [1, 2, 1] ], \
			[ [-1, 0, 1], [-2, 0, 2], [-1, 0, 1] ]]

	return edge_detect(pix, size, mask, thres, 'sum')

def	FreiChen(pix, size, thres):
	mask = [[ [-1, -sqrt(2), -1], [0, 0, 0], [1, sqrt(2), 1] ], \
			[ [-1, 0, 1], [-sqrt(2), 0, sqrt(2)], [-1, 0, 1] ]]

	return edge_detect(pix, size, mask, thres, 'sum')

def	Kirsch(pix, size, thres):
	mask = [[ [-3, -3, 5], [-3, 0, 5], [-3, -3, 5] ], \
			[ [-3, 5, 5], [-3, 0, 5], [-3, -3, -3] ], \
			[ [5, 5, 5], [-3, 0, -3], [-3, -3, -3] ], \
			[ [5, 5, -3], [5, 0, -3], [-3, -3, -3] ], \
			[ [5, -3, -3], [5, 0, -3], [5, -3, -3] ], \
			[ [-3, -3, -3], [5, 0, -3], [5, 5, -3] ], \
			[ [-3, -3, -3], [-3, 0, -3], [5, 5, 5] ], \
			[ [-3, -3, -3], [-3, 0, 5], [-3, 5, 5] ]]
			 
	return edge_detect(pix, size, mask, thres, 'max')

def	Robinson(pix, size, thres):	 
	mask = [[ [-1, 0, 1], [-2, 0, 2], [-1, 0, 1] ], \
			[ [0, 1, 2], [-1, 0, 1], [-2, -1, 0] ], \
			[ [1, 2, 1], [0, 0, 0], [-1, -2, -1] ], \
			[ [2, 1, 0], [1, 0, -1], [0, -1, -2] ], \
			[ [1, 0, -1], [2, 0, -2], [1, 0, -1] ], \
			[ [0, -1, -2], [1, 0, -1], [2, 1, 0] ], \
			[ [-1, -2, -1], [0, 0, 0], [1, 2, 1] ], \
			[ [-2, -1, 0], [-1, 0, 1], [0, 1, 2] ]]

	return edge_detect(pix, size, mask, thres, 'max')

def NB(pix, size, thres):
	mask = [ [[ 100,  100,  100,  100,  100], 
			  [ 100,  100,  100,  100,  100],
			  [   0,    0,    0,    0,    0],
			  [-100, -100, -100, -100, -100], 
			  [-100, -100, -100, -100, -100]], \

		     [[ 100,  100,  100,  100,  100], 
			  [ 100,  100,  100,   78,  -32],
			  [ 100,   92,    0,  -92, -100],
			  [  32,  -78, -100, -100, -100], 
			  [-100, -100, -100, -100, -100]], \

			 [[ 100,  100,  100,   32, -100], 
			  [ 100,  100,   92,  -78, -100],
			  [ 100,  100,    0, -100, -100],
			  [ 100,  -78,  -92, -100, -100], 
			  [-100,  -32, -100, -100, -100]], \

			 [[-100, -100,    0,  100,  100], 
			  [-100, -100,    0,  100,  100],
			  [-100, -100,    0,  100,  100],
			  [-100, -100,    0,  100,  100], 
			  [-100, -100,    0,  100,  100]], \

			 [[-100,   32,  100,  100,  100], 
			  [-100,  -78,   92,  100,  100],
			  [-100, -100,    0,  100,  100],
			  [-100, -100,  -92,   78,  100], 
			  [-100, -100, -100,  -32,  100]], \

			 [[ 100,  100,  100,  100,  100], 
			  [ -32,   78,  100,  100,  100],
			  [-100,  -92,    0,   92,  100],
			  [-100, -100, -100,  -78,   32], 
			  [-100, -100, -100, -100, -100]]]
			 
	return edge_detect(pix, size, mask, thres, 'max')

def main():
	parser = argparse.ArgumentParser(description='Edge detectors')
	parser.add_argument('-input', action='store', dest='input', \
						help='Input image', required=True)
	parser.add_argument('-output', action='store', dest='output', \
						help='Output image', required=True)
	parser.add_argument('-method', action='store', dest='method', \
						help='Method of edge detector', required=True, 
						choices=['Roberts', 'Prewitt', 'Sobel', \
						'FreiChen', 'Kirsch', 'Robinson', 'NB'])
	parser.add_argument('-thres', action='store', type=int, dest='thres', \
						help='Threshold (default 30)', default=30)
	args = parser.parse_args()
	
	try:
		ImageIn = Image.open(args.input)
	except Exception as e:
		print('Cannot open {}.'.format(args.input), file=sys.stderr)
		exit(1)

	thres = args.thres
	size = ImageIn.size
	pixIn = ImageIn.load()

	if args.method == 'Roberts':
		ret = Roberts(pixIn, size, thres)
	elif args.method == 'Prewitt':
		ret = Prewitt(pixIn, size, thres)
	elif args.method == 'Sobel':
		ret = Sobel(pixIn, size, thres)
	elif args.method == 'FreiChen':
		ret = FreiChen(pixIn, size, thres)
	elif args.method == 'Kirsch':
		ret = Kirsch(pixIn, size, thres)
	elif args.method == 'Robinson':
		ret = Robinson(pixIn, size, thres)
	elif args.method == 'NB':
		ret = NB(pixIn, size, thres)

	ImageOut = Image.new('1', size)
	pixOut = ImageOut.load()
	for (k, v) in ret.items():
		pixOut[k] = v 
	ImageOut.save(args.output)
	
if __name__ == '__main__':
	main()