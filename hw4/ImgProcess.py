import sys
from PIL import Image

sumTuple = lambda a, b: (a[0]+b[0], a[1]+b[1]) # element-wise add two tuples

BLACK, WHITE = 0, 255

def dilation(pix, size, kernel):
	width, height = size
	ret = {(x, y): BLACK for x in range(width) for y in range(height)}

	for x in range(width):
		for y in range(height):
			if pix[x, y] == WHITE:
				for _ in kernel:
					keyx, keyy = sumTuple((x, y), _)
					if keyx < 0 or keyx >= width or keyy < 0 or keyy >= height:
						continue
					else:
						ret[keyx, keyy] = WHITE

	return ret

def erosion(pix, size, kernel):
	width, height = size
	ret = {(x, y): BLACK for x in range(width) for y in range(height)}

	total = len(kernel)
	for x in range(width):
		for y in range(height):
			sum = 0
			for _ in kernel:
				keyx, keyy = sumTuple((x, y), _)
				if keyx < 0 or keyx >= width or keyy < 0 or keyy >= height or pix[keyx, keyy] == BLACK:
					break
				elif pix[keyx, keyy] == WHITE:
					sum += 1
			if sum == total:
				ret[x, y] = WHITE

	return ret

def opening(pix, size, kernel):
	ret = erosion(pix, size, kernel)
	return dilation(ret, size, kernel)

def closing(pix, size, kernel):
	ret = dilation(pix, size, kernel)
	return erosion(ret, size, kernel)

def hitAndmiss(pix, size, kernelJ, kernelK):
	width, height = size
	pixComplement = {}
	for x in range(width):
		for y in range(height):
			pixComplement[x, y] = BLACK if pix[x, y] == WHITE else WHITE

	temp1 = erosion(pix, size, kernelJ)
	temp2 = erosion(pixComplement, size, kernelK)

	ret = {}
	for x in range(width):
		for y in range(height):
			if temp1[x, y] == WHITE and temp2[x, y] == WHITE:
				ret[x, y] = WHITE
			else:
				ret[x, y] = BLACK
	return ret

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

	kernelJ = [(-1,  0), (0,  0),
						 (0,  1)]

	kernelK = [(0, -1), (1, -1),
						(1,  0)]

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
	elif sys.argv[1] == 'hitmiss':
		ret = hitAndmiss(pixIn, size, kernelJ, kernelK)
	else:
		sys.stderr.write('OPTION is dilation, erosion, opening or closing.\n')

	for x in range(imgIn.width):
		for y in range(imgIn.height):
			pixOut[x, y] = ret[x, y]

	imgOut.save(sys.argv[3], 'bmp')