import argparse
from math import sqrt, pi, e
from itertools import product
from PIL import Image

BLACK, WHITE = 0, 255

sumTuple = lambda a, b: (a[0]+b[0], a[1]+b[1])

_8NEIGHBOR = [(-1, -1), (0, -1), (1, -1),
			  (-1,  0),          (1,  0),
			  (-1,  1), (0,  1), (1,  1)]

def flip(p, bound):
	if p < 0:
		return -p-1
	elif p >= bound:
		return 2 * bound - 1 - p

	return p

def convolve(M, size, pos, mask):
	ret = 0;
	X, Y = int(len(mask)/2), int(len(mask[0])/2)
	for (j, row) in enumerate(mask):
		for (i, value) in enumerate(row):
			offset = (i-X, j-Y)
			(x, y) = sumTuple(pos, offset)
			x = flip(x, size[0])
			y = flip(y, size[1])
			ret += M[x, y] * value
	
	return ret

def convolve_whole(pix, size, mask):
	return {p: convolve(pix, size, p, mask) \
				for p in product(range(size[0]), range(size[1]))}

def zero_crossing(M, size, thres):
	ret = {}
	for pos in product(range(size[0]), range(size[1])):
		ret[pos] = WHITE
		for offset in _8NEIGHBOR:
			cur = M[pos]
			try:
				neighbor = M[sumTuple(pos, offset)]
				if (cur > thres and neighbor < -thres):
					ret[pos] = BLACK
			except:
				pass

	return ret

def Laplacian(pix, size, kernel, thres):
	mask = [[ [0, 1, 0], [1, -4, 1], [0, 1, 0] ], \
			[ [1/3, 1/3, 1/3], [1/3, -8/3, 1/3], [1/3, 1/3, 1/3]]]

	return zero_crossing(convolve_whole(pix, size, mask[kernel]), size, thres)

def min_var_Laplacian(pix, size, thres):
	mask = [[2/3, -1/3, 2/3], [-1/3, -4/3, -1/3], [2/3, -1/3, 2/3]]

	return zero_crossing(convolve_whole(pix, size, mask), size, thres)

def LOG(pix, size, thres):
	mask = [[ 0,  0,   0,  -1,  -1,  -2,  -1,  -1,   0,  0,  0], 
			[ 0,  0,  -2,  -4,  -8,  -9,  -8,  -4,  -2,  0,  0],
			[ 0, -2,  -7, -15, -22, -23, -22, -15,  -7, -2,  0],
			[-1, -4, -15, -24, -14,  -1, -14, -24, -15, -4, -1],
			[-1, -8, -22, -14,  52, 103,  52, -14, -22, -8, -1],
			[-2, -9, -23,  -1, 103, 178, 103,  -1, -23, -9, -2],
			[-1, -8, -22, -14,  52, 103,  52, -14, -22, -8, -1],
			[-1, -4, -15, -24, -14,  -1, -14, -24, -15, -4, -1],
			[ 0, -2,  -7, -15, -22, -23, -22, -15,  -7, -2,  0],
			[ 0,  0,  -2,  -4,  -8,  -9,  -8,  -4,  -2,  0,  0],
			[ 0,  0,   0,  -1,  -1,  -2,  -1,  -1,   0,  0,  0]]

	return zero_crossing(convolve_whole(pix, size, mask), size, thres)

def Gaussian(x, mean, std):
	return (1 / (sqrt(2 * pi) * std )) * \
			e ** ( (-(x - mean) ** 2 ) / (2 * std ** 2))

def Gaussian2d(x, y, std_x, std_y, mean_x=0, mean_y=0):
	return Gaussian(x, mean_x, std_x) * Gaussian(y, mean_y, std_y);

def DOG_mask(in_sigma, ex_sigma, size=11):
	l = int(-size / 2)
	r = int(size / 2) + 1

	mask = []
	for i, x in enumerate(range(l, r)):
		mask.append([])
		for y in range(l, r):
			mask[i].append(Gaussian2d(x, y, std_x=in_sigma, std_y=in_sigma) \
							-Gaussian2d(x, y, std_x=ex_sigma, std_y=ex_sigma))

	return mask

def DOG(pix, size, in_sigma, ex_sigma, thres):
	mask = DOG_mask(in_sigma, ex_sigma)

	return zero_crossing(convolve_whole(pix, size, mask), size, thres)

def main():
	parser = argparse.ArgumentParser(description='Zero-Crossing Edge detectors')
	parser.add_argument('-input', action='store', dest='input', \
						help='Input image', required=True)
	parser.add_argument('-output', action='store', dest='output', \
						help='Output image', required=True)
	parser.add_argument('-method', action='store', dest='method', \
						help='Method of zero-crossing edge detector', required=True, \
						choices=['Laplacian', 'min-var-Laplacian', 'LOG', 'DOG'])
	parser.add_argument('-kernel', action='store', type=int, dest='kernel', \
						help='Type of kernel for Laplacian', default=0, \
						choices=[0, 1])
	parser.add_argument('-in-sigma', action='store', type=int, dest='in_sigma', \
						help='Inhibitory sigma for DOG (default 1)', default=1)
	parser.add_argument('-ex-sigma', action='store', type=int, dest='ex_sigma', \
						help='excitatory sigma for DOG (default 1)', default=3)
	parser.add_argument('-thres', action='store', type=int, dest='thres', \
						help='Threshold (default 20)', default=20)
	args = parser.parse_args()
	
	try:
		ImageIn = Image.open(args.input)
	except Exception as e:
		print('Cannot open {}.'.format(args.input), file=sys.stderr)
		exit(1)

	thres = args.thres
	size = ImageIn.size
	pixIn = ImageIn.load()

	if args.method == 'Laplacian':
		ret = Laplacian(pixIn, size, args.kernel, thres)
	elif args.method == 'min-var-Laplacian':
		ret = min_var_Laplacian(pixIn, size, thres)
	elif args.method == 'LOG':
		ret = LOG(pixIn, size, thres)
	elif args.method == 'DOG':
		ret = DOG(pixIn, size, args.in_sigma, args.ex_sigma, thres)

	ImageOut = Image.new('1', size)
	pixOut = ImageOut.load()
	for (k, v) in ret.items():
		pixOut[k] = v 
	ImageOut.save(args.output)
	
if __name__ == '__main__':
	main()