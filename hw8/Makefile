all: noisy removal

removal: box median

noisy: gaussian salt_pepper open_close close_open

salt_pepper:
	python3 noisy-image.py lena.bmp lena-salt-pepper-01.bmp salt_pepper 0.2
	python3 noisy-image.py lena.bmp lena-salt-pepper-005.bmp salt_pepper 0.1

gaussian:
	python3 noisy-image.py lena.bmp lena-gaussian-10.bmp gaussian 10
	python3 noisy-image.py lena.bmp lena-gaussian-30.bmp gaussian 30

box:
	python3 noise-removal.py lena-gaussian-10.bmp lena-gaussian-10-box-3x3.bmp box 3
	python3 noise-removal.py lena-gaussian-10.bmp lena-gaussian-10-box-5x5.bmp box 5
	python3 noise-removal.py lena-gaussian-30.bmp lena-gaussian-30-box-3x3.bmp box 3
	python3 noise-removal.py lena-gaussian-30.bmp lena-gaussian-30-box-5x5.bmp box 5
	python3 noise-removal.py lena-salt-pepper-01.bmp lena-salt-pepper-01-box-3x3.bmp box 3
	python3 noise-removal.py lena-salt-pepper-01.bmp lena-salt-pepper-01-box-5x5.bmp box 5
	python3 noise-removal.py lena-salt-pepper-005.bmp lena-salt-pepper-005-box-3x3.bmp box 3
	python3 noise-removal.py lena-salt-pepper-005.bmp lena-salt-pepper-005-box-5x5.bmp box 5

median:
	python3 noise-removal.py lena-gaussian-10.bmp lena-gaussian-10-median-3x3.bmp median 3
	python3 noise-removal.py lena-gaussian-10.bmp lena-gaussian-10-median-5x5.bmp median 5
	python3 noise-removal.py lena-gaussian-30.bmp lena-gaussian-30-median-3x3.bmp median 3
	python3 noise-removal.py lena-gaussian-30.bmp lena-gaussian-30-median-5x5.bmp median 5
	python3 noise-removal.py lena-salt-pepper-01.bmp lena-salt-pepper-01-median-3x3.bmp median 3
	python3 noise-removal.py lena-salt-pepper-01.bmp lena-salt-pepper-01-median-5x5.bmp median 5
	python3 noise-removal.py lena-salt-pepper-005.bmp lena-salt-pepper-005-median-3x3.bmp median 3
	python3 noise-removal.py lena-salt-pepper-005.bmp lena-salt-pepper-005-median-5x5.bmp median 5

open_close:
	python3 noise-removal.py lena-gaussian-10.bmp lena-gaussian-10-open-close.bmp open_close
	python3 noise-removal.py lena-gaussian-30.bmp lena-gaussian-30-open-close.bmp open_close
	python3 noise-removal.py lena-salt-pepper-01.bmp lena-salt-pepper-01-open-close.bmp open_close
	python3 noise-removal.py lena-salt-pepper-005.bmp lena-salt-pepper-005-open-close.bmp open_close


close_open:
	python3 noise-removal.py lena-gaussian-10.bmp lena-gaussian-10-close-open.bmp close_open
	python3 noise-removal.py lena-gaussian-30.bmp lena-gaussian-30-close-open.bmp close_open
	python3 noise-removal.py lena-salt-pepper-01.bmp lena-salt-pepper-01-close-open.bmp close_open
	python3 noise-removal.py lena-salt-pepper-005.bmp lena-salt-pepper-005-close-open.bmp close_open

SNR:
	@python3 SNR.py lena.bmp lena-salt-pepper-005-box-3x3.bmp
	@python3 SNR.py lena.bmp lena-salt-pepper-005-box-5x5.bmp
	@python3 SNR.py lena.bmp lena-salt-pepper-005-median-3x3.bmp
	@python3 SNR.py lena.bmp lena-salt-pepper-005-median-5x5.bmp
	@python3 SNR.py lena.bmp lena-salt-pepper-005-open-close.bmp
	@python3 SNR.py lena.bmp lena-salt-pepper-005-close-open.bmp

	@python3 SNR.py lena.bmp lena-salt-pepper-01-box-3x3.bmp
	@python3 SNR.py lena.bmp lena-salt-pepper-01-box-5x5.bmp
	@python3 SNR.py lena.bmp lena-salt-pepper-01-median-3x3.bmp
	@python3 SNR.py lena.bmp lena-salt-pepper-01-median-5x5.bmp
	@python3 SNR.py lena.bmp lena-salt-pepper-01-open-close.bmp
	@python3 SNR.py lena.bmp lena-salt-pepper-01-close-open.bmp

	@python3 SNR.py lena.bmp lena-gaussian-10-box-3x3.bmp
	@python3 SNR.py lena.bmp lena-gaussian-10-box-5x5.bmp
	@python3 SNR.py lena.bmp lena-gaussian-10-median-3x3.bmp
	@python3 SNR.py lena.bmp lena-gaussian-10-median-5x5.bmp
	@python3 SNR.py lena.bmp lena-gaussian-10-open-close.bmp
	@python3 SNR.py lena.bmp lena-gaussian-10-close-open.bmp

	@python3 SNR.py lena.bmp lena-gaussian-30-box-3x3.bmp
	@python3 SNR.py lena.bmp lena-gaussian-30-box-5x5.bmp
	@python3 SNR.py lena.bmp lena-gaussian-30-median-3x3.bmp
	@python3 SNR.py lena.bmp lena-gaussian-30-median-5x5.bmp
	@python3 SNR.py lena.bmp lena-gaussian-30-open-close.bmp
	@python3 SNR.py lena.bmp lena-gaussian-30-close-open.bmp