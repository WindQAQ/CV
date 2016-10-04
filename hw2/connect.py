import sys, math
from PIL import Image, ImageDraw

class DisJoint:
	def __init__(self):
		self.p = {}
		self.size = {}
	
	def make(self, x):
		self.p[x] = x
		self.size[x] = 1

	def find(self, x):
		if x == self.p[x]:
			return x
		else:
			self.p[x] = self.find(self.p[x])
			return self.p[x]

	def union(self, x, y):
		X, Y = self.find(self.p[x]), self.find(self.p[y])
		if X == Y:
			return

		if self.size[X] >= self.size[Y]:
			self.size[X] += self.size[Y]
			self.p[Y] = X
		else:
			self.size[Y] += self.size[X]
			self.p[X] = Y

	def getsize(self, x):
		return self.size[self.find(x)]

	def increase(self, x):
		self.size[self.find(x)] += 1

class Component:
	def __init__(self):
		self.up = self.left = float('inf')
		self.low = self.right = -float('inf')
		self.X = 0
		self.Y = 0
		self.A = 0

	def add(self, x, y):
		self.up = min(self.up, y)
		self.low = max(self.low, y)
		self.left = min(self.left, x)
		self.right = max(self.right, x)
		self.X += x
		self.Y += y
		self.A += 1

	def getbound(self):
		return [self.left, self.up, self.right, self.low]

	def getcentroid(self):
		return ((self.X/self.A), (self.Y/self.A))

def drawPlus(draw, centroid, color):
	l = 7
	x, y = centroid
	draw.line((x-l, y, x+l, y), fill=color)
	draw.line((x, y-l, x, y+l), fill=color)

def Label(img):
	pix = img.load()	
	width, height = img.size
	
	Eq = DisJoint()

	labels = {}
	stamp = 1

	for y in range(height):
		for x in range(width):
			if pix[x, y] == 0:
				labels[x, y] = 0 # background
				continue
			
			left = labels[x-1, y] if x-1 >= 0 else 0
			top = labels[x, y-1] if y-1 >= 0 else 0
			
			if left == 0 and top == 0:
				labels[x, y] = stamp
				Eq.make(stamp)
				stamp += 1
			elif left != 0 and top != 0:
				labels[x, y] = left if left < top else top
				if left != top:
					Eq.union(left, top)
				Eq.increase(labels[x, y])
			else:
				labels[x, y] = left if left != 0 else top
				Eq.increase(labels[x, y])
	
	return Eq, labels

def Last(img, Eq, labels):
	width, height = img.size
	
	out = Image.new('RGB', img.size)
	pix = out.load()
	
	Group = {}
	for y in range(height):
		for x in range(width):
			if labels[x, y] != 0:
				n = Eq.find(labels[x, y])
				if Eq.getsize(n) >= 500:
					if n not in Group:
						Group[n] = Component()
					Group[n].add(x, y)
				pix[x, y] = (255, 255, 255)
			else:
				pix[x, y] = (0, 0, 0)

	draw = ImageDraw.Draw(out)
	colorP, colorR = (255, 0, 0), (220, 116, 246)
	for i in Group:
		drawPlus(draw, Group[i].getcentroid(), colorP)
		draw.rectangle(Group[i].getbound(), fill=None, outline=colorR)

	return out

def CC(img):
	Eq, labels = Label(img)
	out = Last(img, Eq, labels)
	out.save(sys.argv[2], 'bmp')

if __name__ == '__main__':
	try:
		img = Image.open(sys.argv[1])
	except:
		print ("Fail to open", sys.argv[1])
		exit()

	# find connected components
	CC(img)
