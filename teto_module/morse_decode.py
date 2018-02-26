# temp = open('groups_detail.txt', 'w')
# samplingdata = open('sampling_data.txt', "w")
# signalsdata = open('signals_data.txt', "w")

def remove_pointy_peaks(data):
	# remove zero sequences in data if that sequence has length < 3
	_data = data
	for i, dot in enumerate(_data):
		if _data[i] == 0 and _data[i - 1] != 0 and (_data[i + 1] != 0 or _data[i + 2] != 0):
			_data[i] = _data[i - 1]
	return _data

def get_message_start(max_hightime, data):
	# We already know max_hightime in data at this point
	count_hightime = 0

	for message_start_position, dot in enumerate(data):
		if dot == 0:
			if count_hightime == max_hightime:
				return message_start_position
			count_hightime = 0
		else:
			count_hightime += 1

	# Aka not found
	return len(data)


def separate_into_signals(data, message_start):
	signals = []
	start = 0
	end = 0 

	for i in range(message_start, len(data)):
		if (i < end):
			continue

		# Get the start of a morse signal
		start = i
		while start < len(data) and data[start] == 0:
			start += 1

		# Get the end of a morse signal
		end = start
		while (end < len(data)) and (data[end] != 0):
			end += 1		

		# Add pair (start, end) of a signal to detected signals
		signals.append((start, end - 1))
		# print("Sig [%s..%s]"%(start, end - 1), file = signalsdata)
	return signals

def get_average(signals):
	average_len = 0
	for (first, last) in signals:		
		average_len += (last - first + 1)		
	#  ** Handle the division by zero here!!
	average_len /= len(signals)
	return average_len

def combine_into_morse_group(signals):
	# Separate into group
	groups = []
	ngroup = 0
	pfirst = plast = 0
	i = 0
	pre_dis = 30
	while i < len(signals) - 1:		
		g = [(signals[i][0], signals[i][1])]
		current_dis = signals[i + 1][0] - signals[i][1]
		while (current_dis - pre_dis <= 40) and (current_dis > 10):
			g.append((signals[i + 1][0], signals[i + 1][1]))
			i += 1
			pre_dis = current_dis
			current_dis = signals[i + 1][0] - signals[i][1]
		i += 1
		groups.append(g)

	# for group in groups:
	# 	print("Group:", file = temp)
	# 	for (first, end) in group:
	# 		print("[%s..%s]" %(first, end), file = temp)

	return groups

def translate_to_morse(signals, groups):
	morse = ""
	average_len = get_average(signals)
	for char in groups:
		for (start, end) in char:
			if end - start <= average_len and end - start > 5:
				morse += '.'
			else:
				if end - start > average_len:
					morse += '-'
		morse += " "

	return morse

def morse_from_mono_wave(data):	

	# Make data more smooth
	data = remove_pointy_peaks(data)

	# Calculating longest and shortest HIGH segment	
	count = 0
	max_hightime = 0
	min_hightime = 10000000	
	for x in data:
		# print("Sampling %s" % x, file = samplingdata)
		if (x == 0):
			max_hightime = max(max_hightime, count)
			if (count != 0) and (count > 10):
				min_hightime = min(min_hightime, count)
			count = 0
		else:
			count += 1
	print("(morse_decode) max_hightime: %s min_hightime: %s" % (max_hightime, min_hightime))

	# Get the starting point of message < definite as a long dahhhhhh >
	message_start = get_message_start(max_hightime, data)
	print("(morse_decode) message_start: %s" % (message_start))

	# Separate into signals list
	signals = separate_into_signals(data, message_start)

	# Now, a signal is a dih if it's <= average_len
	# Divide signals into group (character)
	groups = combine_into_morse_group(signals)
	morse_result = translate_to_morse(signals, groups)


	return morse_result

