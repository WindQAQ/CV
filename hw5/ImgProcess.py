import sys
from PIL import Image

sumTuple = lambda a, b: (a[0]+b[0], a[1]+b[1]) # element-wise add two tuples

BLACK, WHITE = 0, 255

def dilation(pix, size, kernel):
	width, height = size
	ret = {(x, y): BLACK for x in range(width) for y in range(height)}

	for x in range(width):
		for y in range(height):
			for _ in kernel:
				X, Y = sumTuple((x, y), _)
				if 0 <= X < width and 0 <= Y < height:
					ret[x, y] = max(ret[x, y], pix[X, Y])

	return ret

def erosion(pix, size, kernel):
	width, height = size
	ret = {(x, y): WHITE for x in range(width) for y in range(height)}

	for x in range(width):
		for y in range(height):
			for _ in kernel:
				X, Y = sumTuple((x, y), _)
				if 0 <= X < width and 0 <= Y < height:
					ret[x, y] = min(ret[x, y], pix[X, Y])

	return ret

def opening(pix, size, kernel):
	return dilation(erosion(pix, size, kernel), size, kernel)

def closing(pix, size, kernel):
	return erosion(dilation(pix, size, kernel), size, kernel)

if __name__ == '__main__':

	if len(sys.argv) != 4:
		sys.stderr.write('Usage: python3 ImgProcess.py OPTION IMG_IN IMG_OUT\n')
		exit()
	try:
		imgIn = Image.open(sys.argv[2])
	except:
		sys.stderr.write("Fail to open {}.\n".format(sys.argv[2]))
		exit()

	kernel = [(-1, -2), (0, -2), (1, -2), 
	(-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
	(-2,  0), (-1,  0), (0,  0), (1,  0), (2,  0),
	(-2,  1), (-1,  1), (0,  1), (1,  1), (2,  1),
			  (-1,  2), (0,  2), (1,  2)]

	size = imgIn.size
	imgOut = Image.new(imgIn.mode, imgIn.size)
	pixIn, pixOut = imgIn.load(), imgOut.load()

	if sys.argv[1] == 'dilation':
		ret = dilation(pixIn, size, kernel)
	elif sys.argv[1] == 'erosion':
		ret = erosion(pixIn, size, kernel)
	elif sys.argv[1] == 'opening':
		ret = opening(pixIn, size, kernel)
	elif sys.argv[1] == 'closing':
		ret = closing(pixIn, size, kernel)
	else:
		sys.stderr.write('OPTION can be dilation, erosion, opening or closing.\n')

	for x in range(imgIn.width):
		for y in range(imgIn.height):
			pixOut[x, y] = ret[x, y]

	imgOut.save(sys.argv[3], 'bmp')