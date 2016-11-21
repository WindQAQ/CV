import sys
from itertools import product
from PIL import Image

BLACK, WHITE = 0, 255

BLOCK_1 = [(0, 0), ( 1,  0), ( 1, -1), ( 0, -1)]
BLOCK_2 = [(0, 0), ( 0, -1), (-1, -1), (-1,  0)]
BLOCK_3 = [(0, 0), (-1,  0), (-1,  1), ( 0,  1)]
BLOCK_4 = [(0, 0), ( 0,  1), ( 1,  1), ( 1,  0)]
BLOCK = [BLOCK_1, BLOCK_2, BLOCK_3, BLOCK_4]

q, r, s = 1, 0, -1

def downsample(pix, size, BLOCK_LEN):
	width, height = int(size[0] / BLOCK_LEN), int(size[1] / BLOCK_LEN)
	
	calPos = lambda x: (x[0]*BLOCK_LEN, x[1]*BLOCK_LEN)
	M = {_: pix[calPos(_)] for _ in product(range(width), range(height))}
	
	return M, (width, height)

def h(M, B):
	if M[B[0]] != M[B[1]]:
		return s
	elif M[B[0]] == M[B[1]] == M[B[2]] == M[B[3]]:
		return r
	else:
		return q

def f(a):
	if a[0] == a[1] == a[2] == a[3] == r:
		return 5
	else:
		return a.count(q)

def sumTuple(x, y):
	return (x[0]+y[0], x[1]+y[1])

def translation(M, cur):
	ret = {}

	for _ in product(range(-1, 2), repeat=2):
		pos = sumTuple(cur, _)
		try:
			ret[_] = M[pos]
		except:
			ret[_] = BLACK

	return ret

def Yokoi(M, size):
	ret = {}
	width, height = size
	for cur in product(range(width), range(height)):
		if M[cur] == WHITE:
			T = translation(M, cur)
			ret[cur] = f([h(T, B) for B in BLOCK])
		else:
			ret[cur] = ' '
	return ret

def write2file(f, Y, size):
	width, height = size

	for y in range(height):
		for x in range(width):
			end = '\n' if x == width-1 else ''
			f.write('{}{}'.format(Y[x, y], end))

def main():
	if len(sys.argv) != 3:
		sys.stderr.write('Usage: python3 Yokoi.py IMG_IN FILE_OUT\n')
		exit()
	try:
		imgIn = Image.open(sys.argv[1])
	except:
		sys.stderr.write("Fail to open {}.\n".format(sys.argv[1]))
		exit()

	size = imgIn.size
	pixIn= imgIn.load()
	BLOCK_LEN = 8

	M, shrinkSize = downsample(pixIn, size, BLOCK_LEN)

	Y = Yokoi(M, shrinkSize)
	
	with open(sys.argv[2], 'w') as f:
		write2file(f, Y, shrinkSize)

if __name__ == '__main__':
	main()
