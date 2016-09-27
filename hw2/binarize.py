import sys
from PIL import Image

try:
	original = Image.open(sys.argv[1])
except:
	print ("Fail to open", sys.argv[1])
	exit()

binary = Image.new('1', original.size)

pix_ori, pix_b = original.load(), binary.load()

width, height = original.width, original.height

for x in range(0, width):
	for y in range(0, height):
		pix_b [x, y] = 1 if pix_ori[x, y] >= 128 else 0

binary.save(sys.argv[2], 'bmp')
