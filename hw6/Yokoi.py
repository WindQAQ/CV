import sys
from itertools import product
from PIL import Image

def downsample(pix, size, BLOCK_LEN):
	width, height = size[0] / BLOCK_LEN, size[1] / BLOCK_LEN
	calPos = lambda x: x[0]*BLOCK_LEN, x[1]*BLOCK_LEN
	M = {pix[calPos(_)] for _ in product(range(width), range(height))}
	return M, (width, height)

def Yokoi(M, size):
	BLOCK_1 = [(0, 0), ( 1,  0), ( 1, -1), ( 0, -1)]
	BLOCK_2 = [(0, 0), ( 0, -1), (-1, -1), (-1,  0)]
	BLOCK_3 = [(0, 0), (-1,  0), (-1,  1), ( 0,  1)]
	BLOCK_4 = [(0, 0), ( 0,  1), ( 1,  1), ( 1,  0)]

def main():
	if len(sys.argv) != 3:
		sys.stderr.write('Usage: python3 Yokoi.py IMG_IN FILE_OUT\n')
		exit()
	try:
		imgIn = Image.open(sys.argv[1])
	except:
		sys.stderr.write("Fail to open {}.\n".format(sys.argv[2]))
		exit()

	size = imgIn.size
	pixIn= imgIn.load()
	BLOCK_LEN = 8

	M, shrinkSize = downsample(pixIn, size, BLOCK_LEN)

	Y = Yokoi(M, shrinkSize)

if __name__ == '__main__':
	main()
