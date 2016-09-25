import sys
from PIL import Image

try:
	original = Image.open(sys.argv[1])
except:
	print ("Fail to open", sys.argv[1])
	exit()

upside_down = Image.new(original.mode, original.size)

pix_ori, pix_ud = original.load(), upside_down.load()

width, height = original.width, original.height

for x in range(0, width):
	for y in range(0, height):
		pix_ud [x, y] = pix_ori[x, height-y-1]

upside_down.save(sys.argv[2])
