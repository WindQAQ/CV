import sys
from PIL import Image

def label(table, X, Y):
	equiv = {}
	stamp = 1
	for x in range(X):
		for y in range(Y):
			if table[x, y] == 0:
				continue
			
			left = table[x-1, y] if (x-1, y) in table else 0
			up = table[x, y-1] if (x, y-1) in table else 0
			
			if left == 0 and up == 0:
				table[x, y] = stamp
				equiv[stamp] = set()
				stamp += 1
			elif left != 0 and up != 0:
				table[x, y] = left if left < up else up
				if left != up:
					equiv[left].add(up)
					equiv[up].add(left)
			else:
				table[x, y] = left if left != 0 else up
	return equiv

try:
	original = Image.open(sys.argv[1])
except:
	print ("Fail to open", sys.argv[1])
	exit()

pix_ori = original.load()

width, height = original.width, original.height

# initialize table
table = {}
for x in range(width):
	for y in range(height):
		table[x, y] = pix_ori[x, y]

# labeling
equiv = label(table, width, height)
