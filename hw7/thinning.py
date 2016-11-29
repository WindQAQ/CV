import sys
from itertools import product
from PIL import Image

BLACK, WHITE = 0, 255

_8NEIGHBOR = [(-1, -1), (0, -1), (1, -1),
			  (-1,  0),          (1,  0),
			  (-1,  1), (0,  1), (1,  1)]

_4NEIGHBOR = [          (0, -1)         ,
			  (-1,  0),          (1,  0),
			            (0,  1)         ]

NEIGHBOR = _8NEIGHBOR

INTERIOR, BORDER, MARKED_BORDER = -1, -2, -3

BLOCK_1 = [(0, 0), ( 1,  0), ( 1, -1), ( 0, -1)]
BLOCK_2 = [(0, 0), ( 0, -1), (-1, -1), (-1,  0)]
BLOCK_3 = [(0, 0), (-1,  0), (-1,  1), ( 0,  1)]
BLOCK_4 = [(0, 0), ( 0,  1), ( 1,  1), ( 1,  0)]
BLOCK = [BLOCK_1, BLOCK_2, BLOCK_3, BLOCK_4]

_3x3BLOCK = [(-1, -1), (0, -1), (1, -1),
			 (-1,  0), (0,  0), (1,  0),
			 (-1,  1), (0,  1), (1,  1)]

g = BLACK

def downsample(pix, size, BLOCK_LEN):
	width, height = int(size[0] / BLOCK_LEN), int(size[1] / BLOCK_LEN)
	
	calPos = lambda x: (x[0]*BLOCK_LEN, x[1]*BLOCK_LEN)
	M = {cur: pix[calPos(cur)] for cur in product(range(width), range(height))}
	
	return M, (width, height)

def sumTuple(x, y):
	return (x[0]+y[0], x[1]+y[1])

def T(M, cur, B):
	ret = {}

	for t in B:
		pos = sumTuple(cur, t)
		try:
			ret[t] = M[pos]
		except:
			ret[t] = BLACK

	return ret

def h(M, B):
	if (M[B[0]] == M[B[1]]) and (M[B[0]] != M[B[2]] or M[B[0]] != M[B[3]]):
		return 1
	else:
		return 0

def f(a):
	if a[:-1].count(1) == 1:
		return g
	else:
		return a[-1]

def mark_interior(M, size):
	width, height = size
	ret = {}
	for cur in product(range(width), range(height)):
		if M[cur] == WHITE:
			trans = T(M, cur, NEIGHBOR)
			if sum(x == WHITE for x in trans.values()) == len(NEIGHBOR):
				ret[cur] = INTERIOR
			else:
				ret[cur] = BORDER
		else:
			ret[cur] = BLACK

	return ret

def pair_rel(M, size):
	width, height = size
	ret = {}
	for cur in product(range(width), range(height)):
		if M[cur] == BORDER:
			trans = T(M, cur, NEIGHBOR)
			if sum(x == INTERIOR for x in trans.values()) >= 1:
				ret[cur] = MARKED_BORDER
			else:
				ret[cur] = WHITE
		elif M[cur] == INTERIOR:
			ret[cur] = WHITE
		else:
			ret[cur] = BLACK

	return ret

def connect_shrink(M, size):
	width, height = size

	for y in range(height):
		for x in range(width):
			cur = (x, y)
			if M[cur] == MARKED_BORDER:
				temp = T(M, cur, _3x3BLOCK)
				trans = {}
				for (k, v) in temp.items():
					trans[k] = WHITE if v == MARKED_BORDER else v
				M[cur] = f([h(trans, B) for B in BLOCK] + [M[cur]])

	ret = {}
	for y in range(height):
		for x in range(width):
			if M[x, y] in [g, BLACK]:
				ret[x, y] = BLACK
			else:
				ret[x, y] = WHITE

	return ret

def thinning(M, size):
	# f = open('test.txt', 'w')
	while True:
		# for y in range(size[0]):
		# 	for x in range(size[1]):
		# 		p = '*' if M[x, y] == WHITE else ' '
		# 		print(p, end='', file=f)
		# 	print('', file=f)

		# print('\n==========================================================================================================================================================================\n', file=f)

		X = mark_interior(M, size)
		Y = pair_rel(X, size)
		ret = connect_shrink(Y, size)

		if ret == M:
			break
		M = ret
	# f.close()
	return ret

def main():
	if len(sys.argv) != 3:
		sys.stderr.write('Usage: python3 thinning.py IMG_IN IMG_OUT\n')
		exit()
	try:
		imgIn = Image.open(sys.argv[1])
	except:
		sys.stderr.write("Fail to open {}.\n".format(sys.argv[1]))
		exit()

	size = imgIn.size
	pixIn= imgIn.load()
	BLOCK_LEN = 8

	M, downSize = downsample(pixIn, size, BLOCK_LEN)

	M = thinning(M, downSize)

	imgOut = Image.new(imgIn.mode, downSize)
	pixOut = imgOut.load()
	for cur in product(range(downSize[0]), range(downSize[1])):
		pixOut[cur] = M[cur]

	imgOut.save(sys.argv[2], 'bmp')

if __name__ == '__main__':
	main()
