import sys
import random
from PIL import Image
from itertools import product

PEPPER, SALT = 0, 255

def gaussian_noise(pix, size, amp):
	ret = {}
	for position in product(range(size[0]), range(size[1])):
		ret[position] = pix[position] + int(amp * random.gauss(0, 1))
	return ret

def salt_pepper(pix, size, prob):
	ret = {}
	for position in product(range(size[0]), range(size[1])):
		r = random.random()
		if r < prob/2:
			ret[position] = PEPPER
		elif r > 1 - prob/2:
			ret[position] = SALT
		else:
			ret[position] = pix[position]
	return ret

def copy(pix, dict_in):
	for (k, v) in dict_in.items():
		pix[k] = v

def main():
	if len(sys.argv) != 5:
		sys.stderr.write('Usage: python3 {} IMG_IN IMG_OUT METHOD VALUE\n'.format(sys.argv[0]))
		exit()
	try:
		imgIn = Image.open(sys.argv[1])
	except:
		sys.stderr.write("Fail to open {}.\n".format(sys.argv[1]))
		exit()

	mode, size = imgIn.mode, imgIn.size
	pixIn = imgIn.load()

	if sys.argv[3] == 'gaussian':
		noise = gaussian_noise(pixIn, size, amp=float(sys.argv[4]))
	elif sys.argv[3] == 'salt_pepper':
		noise = salt_pepper(pixIn, size, prob=float(sys.argv[4]))
	else:
		sys.stderr.write('METHOD can be gaussian or salt_pepper')
		exit()

	imgOut = Image.new(mode, size)
	pixOut = imgOut.load()
	copy(pixOut, noise)
	imgOut.save(sys.argv[2], 'bmp')

if __name__ == '__main__':
	main()