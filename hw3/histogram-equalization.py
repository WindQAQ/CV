import sys
from PIL import Image

import matplotlib.pyplot as plt

try:
	img = Image.open(sys.argv[1])
except:
	print ("Fail to open", sys.argv[1])
	exit()

pix = img.load()

width, height = img.size

N = 256
sum = [0] * N

for x in range(width):
	for y in range(height):
		sum[pix[x, y]] += 1

s = [0] * N
s[0] = sum[0]
for i in range(1, N):
	s[i] = s[i-1] + sum[i]

he = Image.new(img.mode, img.size)
pix_he = he.load()
size = width * height

histogram = [0] * N
for x in range(width):
	for y in range(height):
		pix_he[x, y] = int(255 * s[pix[x, y]] / size)
		histogram[pix_he[x, y]] += 1

fig = plt.figure()
ax = fig.add_subplot(111)

ind = range(N)
plt.bar(ind, histogram, color='black')
ax.set_xlim(0, N-1)
ax.set_xlabel('Value of grayscale')
ax.set_ylabel('Number of pixels')
ax.set_title('Histogram of ' + sys.argv[2])
plt.savefig(sys.argv[3])

he.save(sys.argv[2], 'bmp')
