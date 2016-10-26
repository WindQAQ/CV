import sys
from PIL import Image

kernel = [(-1, -2), (0, -2), (1, -2), 
(-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
(-2,  0), (-1,  0), (0,  0), (1,  0), (2,  0),
(-2,  1), (-1,  1), (0,  1), (1,  1), (2,  1),
		  (-1,  2), (0,  2), (1,  2)]

try:
	img = Image.open(sys.argv[1])
except:
	print ("Fail to open", sys.argv[1])
	exit()

imgO = Image.new(img.mode, img.size, color=0)
width, height = img.size

pix, pixO = img.load(), imgO.load()

sumTuple = lambda a, b: (a[0]+b[0], a[1]+b[1]) # element-wise add two tuples

kernelR = [(-x, -y) for x, y in kernel]
pixT = {(x, y): 255 for x in range(width) for y in range(height)} # temporary pixel map of erosion
for x in range(width):
	for y in range(height):
		for _ in kernelR:
			try:
				if pix[x, y] == 0:
					pixT[sumTuple((x, y), _)] = 0
			except IndexError:
				pass

for x in range(width):
	for y in range(height):
		for _ in kernel:
			try:
				if pixT[x, y] == 255:
					pixO[sumTuple((x, y), _)] = 255
			except IndexError:
				pass

imgO.save(sys.argv[2], 'bmp')