import sys
from itertools import product
from PIL import Image

BLOCK_LEN = 8

def downsample(pix, size):
	width, height = size[0] / BLOCK_LEN, size[1] / BLOCK_LEN
	calPos = lambda x: x[0]*8, x[1]*8
	M = {pix[calPos(_)] for _ in product(range(width), range(height))}
	return M

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

	M = downsample(pixIn, size)

if __name__ == '__main__':
	main()
