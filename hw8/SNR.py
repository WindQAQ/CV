import sys, math
from PIL import Image
from itertools import product

def SNR(S, N, size):
	mean, mean_N = 0, 0
	n = size[0] * size[1]
	for position in product(range(size[0]), range(size[1])):
		mean += S[position]
		mean_N += (N[position] - S[position])

	mean /= n
	mean_N /= n

	VS, VN = 0, 0
	for position in product(range(size[0]), range(size[1])):
		VS += (S[position] - mean) ** 2
		VN += (N[position] - S[position] - mean_N) ** 2
	VS /= n
	VN /= n

	return (10 * math.log10(VS/VN))

def main():
	if len(sys.argv) != 3:
		sys.stderr.write('Usage: python3 {} IMG_S IMG_N\n'.format(sys.argv[0]))
		exit()

	imgS = Image.open(sys.argv[1])
	imgN = Image.open(sys.argv[2])

	snr = SNR(imgS.load(), imgN.load(), imgS.size)

	print('SNR of {} and {} is {}'.format(sys.argv[1], sys.argv[2], snr))

if __name__ == '__main__':
	main()