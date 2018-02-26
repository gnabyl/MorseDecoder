from morse_extract import extract_from_file
from morse_decode import morse_from_mono_wave, remove_pointy_peaks
import matplotlib.pyplot as plt

# Only calculate with frequencies which is
# low < frequency < high
HIGH = 999999
LOW = 16000

# Smaller means you get more peaks 
# To be more clear: not the number of peaks you get
_SKIM = 0.3

# Get morse wave
morse_wave, (t,f,Sxx) = extract_from_file('../resources/morse_namthahnu.wav', low=LOW, high=HIGH)

_max = max(morse_wave)
_min = min(morse_wave)

print('(main.py) max : {}, min: {}'.format(_max, _min))

# If (max+min)>0, we want get a large positive number as skim_frequency
# 	So we divide to a small positive number, means _SKIM
# If (max+min)<0, we want to get a negative number which is close to 0 as skim_frequency
# 	So we divide to a large positive number, means (1/_SKIM)
if (_max+_min)>0:
	skim_frequency = (_max+_min)/_SKIM
else:
	skim_frequency = (_max+_min)/ (1/_SKIM)

for j, dot in enumerate(morse_wave):
	if dot>skim_frequency:
		# 2500 is the value which the blue line in plot will cross. It doesnt hold any meaning in the algorithm.
		morse_wave[j] = 2500
	else:
		morse_wave[j] = 0

print("(morse_decode) %s" % morse_from_mono_wave(morse_wave))

# Plot spectrogram
plt.pcolormesh(t,f,Sxx,nperseg=1000)
# Plot morse
plt.plot(t,remove_pointy_peaks(morse_wave))
plt.show()
