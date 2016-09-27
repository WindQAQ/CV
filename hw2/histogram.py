import sys
from PIL import Image

import matplotlib.pyplot as plt

try:
	original = Image.open(sys.argv[1])
except:
	print ("Fail to open", sys.argv[1])
	exit()

pix_ori = original.load()

width, height = original.width, original.height

N = 256

sum = [0] * N

for x in range(0, width):
	for y in range(0, height):
		sum[pix_ori[x, y]] += 1

fig = plt.figure()
ax = fig.add_subplot(111)

ind = range(N)
plt.bar(ind, sum, color='black')
ax.set_xlim(0, N-1)
ax.set_xlabel('Value of grayscale')
ax.set_ylabel('Number of pixels')
ax.set_title('Histogram of ' + sys.argv[1])

plt.savefig(sys.argv[2])
