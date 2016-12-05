import sys
from PIL import Image
from itertools import product

sumTuple = lambda a, b: (a[0]+b[0], a[1]+b[1]) # element-wise add two tuples

BLACK, WHITE = 0, 255

_35553kernel = [(-1, -2), (0, -2), (1, -2), 
	(-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
	(-2,  0), (-1,  0), (0,  0), (1,  0), (2,  0),
	(-2,  1), (-1,  1), (0,  1), (1,  1), (2,  1),
			  (-1,  2), (0,  2), (1,  2)]

def T(M, cur, B):
	ret = []
	for t in B:
		pos = sumTuple(cur, t)
		try:
			ret.append(M[pos])
		except:
			pass
	return ret

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

def median(list):
	l = len(list)
	if l % 2 == 1:
		return list[int((l+1)/2)-1]
	elif l % 2 == 0:
		return (list[int((l+1)/2)-1] + list[int((l+1)/2)])/2

def box_filter(pix, size, kernel):
	ret = {}
	for position in product(range(size[0]), range(size[1])):
		trans = T(pix, position, kernel)
		ret[position] = int(sum(trans) / len(trans))
	return ret

def median_filter(pix, size, kernel):
	temp = {}
	for position in product(range(size[0]), range(size[1])):
		temp[position] = pix[position]

	ret = {}
	while True:
		for position in product(range(size[0]), range(size[1])):
			ret[position] = int(median(sorted(T(pix, position, kernel))))
		if ret == temp:
			break
		temp = ret

	return ret

def open_close(pix, size, kernel):
	return closing(opening(pix, size, kernel), size, kernel)

def close_open(pix, size, kernel):
	return opening(closing(pix, size, kernel), size, kernel)

def copy(pix, dict_in):
	for (k, v) in dict_in.items():
		pix[k] = v

def main():
	if len(sys.argv) < 4:
		sys.stderr.write('Usage: python3 ImgProcess.py IMG_IN IMG_OUT METHOD [VALUE]\n')
		exit()
	try:
		imgIn = Image.open(sys.argv[1])
	except:
		sys.stderr.write("Fail to open {}.\n".format(sys.argv[1]))
		exit()

	mode, size = imgIn.mode, imgIn.size
	imgOut = Image.new(mode, size)
	pixIn = imgIn.load()

	if sys.argv[3] == 'box':
		s = int(int(sys.argv[4]) / 2)
		kernel = list(product(range(-s, s+1), repeat=2))
		ret = box_filter(pixIn, size, kernel)
	elif sys.argv[3] == 'median':
		s = int(int(sys.argv[4]) / 2)
		kernel = list(product(range(-s, s+1), repeat=2))
		ret = median_filter(pixIn, size, kernel)
	elif sys.argv[3] == 'open_close':
		kernel = _35553kernel
		ret = open_close(pixIn, size, kernel)
	elif sys.argv[3] == 'close_open':
		kernel = _35553kernel
		ret = close_open(pixIn, size, kernel)
	else:
		sys.stderr.write('METHOD can be box, median, open_close or close_open.\n')

	imgOut = Image.new(mode, size)
	pixOut = imgOut.load()
	copy(pixOut, ret)
	imgOut.save(sys.argv[2], 'bmp')

if __name__ == '__main__':
	main()