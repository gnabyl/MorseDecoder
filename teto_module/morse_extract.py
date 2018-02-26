from scipy.io import wavfile
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

def extract_from_file(file, low=0, high=99999999):
	samplingFrequency, signalData = wavfile.read(file)

	# Stereo to Mono
	print('(morse_extract.py) reading from file: {}'.format(file))
	try:
		print('(morse_extract.py) Converting to mono')
		# Try accessing the second channel 
		signalData[0][1]
		signalData = [stereo[0]/2+stereo[1]/2 for stereo in signalData]
		signalData = np.asarray(signalData)
	except:
		print('(morse_extract.py) File already is mono')
	
	# Get spectrogram of raw wave
	f, t, Sxx = signal.spectrogram(signalData, samplingFrequency)
	Sxx = 10 * np.log10(Sxx)

	# Get min of Sxx, min must not be -inf
	_min = np.inf
	for i,row in enumerate(Sxx):
		for j,dot in enumerate(row):
			if dot != -np.inf and dot < _min:
					_min = dot

	# Change -inf to (_min-1) aka smallest value	
	for i,row in enumerate(Sxx):
		for j,dot in enumerate(row):
			if (dot == -np.inf):
					Sxx[i][j] = _min - 1

	# Flatten, return 1D array, _flatten[x] = sum of col x of Sxx
	_flatten = []

	width, height = len(Sxx[0]), len(Sxx)

	for j in range(width):
		col = [Sxx[i][j] for i,frequency in enumerate(f) if low<frequency and frequency<high]
		sum_col = sum(col)
		_flatten.append(sum_col)
	
	return _flatten, (t,f,Sxx)

