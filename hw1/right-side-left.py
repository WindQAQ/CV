import sys
from PIL import Image

try:
	original = Image.open(sys.argv[1])
except:
	print ("Fail to open", sys.argv[1])
	exit()

right_side_left = Image.new(original.mode, original.size)

pix_ori, pix_rl = original.load(), right_side_left.load()

width, height = original.width, original.height

for x in range(0, width):
	for y in range(0, height):
		pix_rl [x, y] = pix_ori[width-x-1, y]

right_side_left.save(sys.argv[2])
