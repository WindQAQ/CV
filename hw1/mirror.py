import sys
from PIL import Image

try:
	original = Image.open(sys.argv[1])
except:
	print ("Fail to open", sys.argv[1])
	exit()

mirror = Image.new(original.mode, original.size)

pix_ori, pix_mir = original.load(), mirror.load()

width, height = original.width, original.height

for x in range(0, width):
	for y in range(0, height):
		pix_mir [x, y] = pix_ori[y, x]

mirror.save(sys.argv[2])
