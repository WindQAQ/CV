import sys
from PIL import Image

sumTuple = lambda a, b: (a[0]+b[0], a[1]+b[1]) # element-wise add two tuples

BLACK, WHITE = 0, 255

def dilation(pix, size, kernel):
	width, height = size
	temp = {(x, y): BLACK for x in range(width) for y in range(height)}

	for x in range(width):
		for y in range(height):
			for _ in kernel:
				try:
					if pix[x, y] == WHITE:
						temp[sumTuple((x, y), _)] = WHITE
				except IndexError:
					pass

	return temp

def erosion(pix, size, kernel):
	width, height = size
	temp = {(x, y): WHITE for x in range(width) for y in range(height)}

	kernelR = [(-x, -y) for x, y in kernel] # reflect each point about origin
	for x in range(width):
		for y in range(height):
			for _ in kernelR:
				try:
					if pix[x, y] == BLACK:
						temp[sumTuple((x, y), _)] = BLACK
				except IndexError:
					pass

	return temp

def opening(pix, size, kernel):
	temp = erosion(pix, size, kernel)
	return dilation(temp, size, kernel)

def closing(pix, size, kernel):
	temp = dilation(pix, size, kernel)
	return erosion(temp, size, kernel)

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
		temp = dilation(pixIn, size, kernel)
	elif sys.argv[1] == 'erosion':
		temp = erosion(pixIn, size, kernel)
	elif sys.argv[1] == 'opening':
		temp = opening(pixIn, size, kernel)
	elif sys.argv[1] == 'closing':
		temp = closing(pixIn, size, kernel)
	else:
		sys.stderr.write('OPTION is dilation, erosion, opening or closing.\n')

	for x in range(imgIn.width):
		for y in range(imgIn.height):
			pixOut[x, y] = temp[x, y]

	imgOut.save(sys.argv[3], 'bmp')