from morse_extract import extract_from_file
import matplotlib.pyplot as plt

# Only calculate with frequencies which is
# low < frequency < high
HIGH = 999999
LOW = 16000

# Smaller means you get more peaks 
# To be more clear: not the number of peaks you get
_SKIM = 0.3

# Get morse wave
morse_wave, (t,f,Sxx) = extract_from_file('./resources/morse_bannghe.wav', low=LOW, high=HIGH)

_max = max(morse_wave)
_min = min(morse_wave)

print('(main.py) max : {}, min: {}'.format(_max, _min))

# If (max+min)>0, we want get a large positive number as skim_frequency
# 	So we divide to a small positive number, means _SKIM
# If (max+min)<0, we want to get a small negative number as skim_frequency
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

# Plot spectrogram
plt.pcolormesh(t,f,Sxx)
# Plot morse
plt.plot(t,morse_wave)
plt.show()
