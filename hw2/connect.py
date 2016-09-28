import sys
from PIL import Image

import random

def Find(p, x):
	if x == p[x]:
		return x
	else:
		p[x] = Find(p, p[x])
		return p[x]

def Union(p, x, y):
	X, Y = Find(p, x), Find(p, y)
	p[X] = Y

def Label(pix, width, height):
	
	p = {}

	labels = {}
	stamp = 1

	for y in range(height):
		for x in range(width):
			if pix[x, y] == 0:
				labels[x, y] = 0
				continue
			
			left = labels[x-1, y] if x-1 >= 0 else 0
			top = labels[x, y-1] if y-1 >= 0 else 0
			
			if left == 0 and top == 0:
				labels[x, y] = stamp
				p[stamp] = stamp
				stamp += 1
			elif left != 0 and top != 0:
				labels[x, y] = left if left < top else top
				if left != top:
					Union(p, left, top)
			else:
				labels[x, y] = left if left != 0 else top
	
	out = Image.new('RGB', (width, height))
	oo = out.load()
	color = {}
	# replace
	for y in range(height):
		for x in range(width):
			if pix[x, y] != 0:
				labels[x, y] = Find(p, labels[x, y])
				if labels[x, y] in color:
					oo[x, y] = color[labels[x, y]]
				else:
					color[labels[x, y]] = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
					oo[x, y] = color[labels[x, y]]
			else:
				oo[x, y] = (0, 0, 0)
	
	out.show()

def CC(img):
	pix = img.load()	
	width, height = img.size

	Label(pix, width, height)
	

try:
	img = Image.open(sys.argv[1])
except:
	print ("Fail to open", sys.argv[1])
	exit()

# find connected components
CC(img)
