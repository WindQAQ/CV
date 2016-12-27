all: run

run: Laplacian0 Laplacian1 min-var-Laplacian LOG DOG

Laplacian0:
	python3.5 zero-crossing-edge-detector.py -input lena.bmp -output lena-laplacian-0.bmp -method Laplacian -kernel 0 -thres 15

Laplacian1:
	python3.5 zero-crossing-edge-detector.py -input lena.bmp -output lena-laplacian-1.bmp -method Laplacian -kernel 1 -thres 15

min-var-Laplacian:
	python3.5 zero-crossing-edge-detector.py -input lena.bmp -output lena-min-var-laplacian.bmp -method min-var-Laplacian -thres 20

LOG:
	python3.5 zero-crossing-edge-detector.py -input lena.bmp -output lena-log.bmp -method LOG -thres 3000

DOG:
	python3.5 zero-crossing-edge-detector.py -input lena.bmp -output lena-dog.bmp -method DOG -in-sigma 1 -ex-sigma 3 -thres 3