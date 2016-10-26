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

imgE = Image.new(img.mode, img.size, color=255)
width, height = img.size

pix, pixE = img.load(), imgE.load()

sumTuple = lambda a, b: (a[0]+b[0], a[1]+b[1]) # element-wise add two tuples

kernelR = [(-x, -y) for x, y in kernel]		   # reflect each point about origin
for x in range(width):
	for y in range(height):
		for _ in kernelR:
			try:
				if pix[x, y] == 0:
					pixE[sumTuple((x, y), _)] = 0
			except IndexError:
				pass

imgE.save(sys.argv[2], 'bmp')