all: run

run:
	python3.5 edge-detector.py -input lena.bmp -output lena-roberts.bmp -method Roberts -thres 12
	python3.5 edge-detector.py -input lena.bmp -output lena-prewitt.bmp -method Prewitt -thres 24
	python3.5 edge-detector.py -input lena.bmp -output lena-sobel.bmp -method Sobel -thres 38
	python3.5 edge-detector.py -input lena.bmp -output lena-freichen.bmp -method FreiChen -thres 30
	python3.5 edge-detector.py -input lena.bmp -output lena-kirsch.bmp -method Kirsch -thres 135
	python3.5 edge-detector.py -input lena.bmp -output lena-robinson.bmp -method Robinson -thres 43
	python3.5 edge-detector.py -input lena.bmp -output lena-nb.bmp -method NB -thres 12500