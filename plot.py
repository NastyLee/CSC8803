import json
import datetime
import matplotlib.pyplot as plt
import statistics
import numpy as np
import pickle



fig = plt.figure(figsize=(12, 6))
positive_graph = fig.add_subplot(111)

data = []
count = 1

thu_data = []
mon_data = []
tue_data = []
wed_data = []
fri_data = []
sat_data = []
sun_data = []

mon_pos = []
mon_neg = []
mon_time = []
tue_pos = []
tue_time = []
wed_pos = []
wed_time = []
thu_pos = []
thu_time =[]
fri_pos = []
fri_time = []
sat_pos = []
sat_time = []
sun_pos = []
sun_time = []


def getKey(item):
	return item[0]

def calculateMeanStd(temp_data):
	return_time = []
	return_pos = []
	temp_data = sorted(temp_data, key = getKey)

	
	t = temp_data[0][0]
	buff=[]

	for i in range(len(temp_data)):
		if temp_data[i][0] == t:
			buff.append(temp_data[i][1])
		else:
			return_time.append(t)
			if len(buff) > 1:	
				return_pos.append([statistics.mean(buff), statistics.stdev(buff)])
			else:
				return_pos.append([buff[0], 0])
			buff = [temp_data[i][0]]
			t = temp_data[i][0]
	return return_time, return_pos


with open('tweet-scores.json') as data_file:  
	for line in data_file: 
		line_data = json.loads(line)
		#line_data['neg']
		pos_score = line_data['neg']
		if pos_score > 0:
			timestamp = datetime.datetime.utcfromtimestamp(int(line_data["local_timestamp_ms"])/1000).strftime('%a %H-%M-%S')
			[day, time] = timestamp.split()
			time = map(int, time.split("-"))
			time = round(time[0] + time[1] / 60.0 + time[2] / 3600.0, 1)
			if day == "Mon":
				mon_data.append([time, pos_score])
			elif day == "Tue":
				tue_data.append([time, pos_score])
			elif day ==  "Wed":
				wed_data.append([time, pos_score])
			elif day ==  "Thu":
				thu_data.append([time, pos_score])
			elif day ==  "Fri":
				fri_data.append([time, pos_score])
			elif day ==  "Sat":
				sat_data.append([time, pos_score])
			else:
				sun_data.append([time, pos_score])

mon_time, mon_pos = calculateMeanStd(mon_data)
tue_time, tue_pos = calculateMeanStd(tue_data)
wed_time, wed_pos = calculateMeanStd(mon_data)
thu_time, thu_pos = calculateMeanStd(thu_data)
fri_time, fri_pos = calculateMeanStd(fri_data)
sat_time, sat_pos = calculateMeanStd(sat_data)
sun_time, sun_pos = calculateMeanStd(sun_data)

pickle.dump([mon_time, mon_pos, tue_time, tue_pos, wed_time, wed_pos, thu_time, thu_pos, fri_time, fri_pos, sat_time, sat_pos, sun_time, sun_pos], open("na.p", "wb" ))



positive_graph.plot(mon_time, np.array(mon_pos)[:, 0], label="Mon")
positive_graph.plot(tue_time, np.array(tue_pos)[:, 0], label="Tue")
positive_graph.plot(wed_time, np.array(wed_pos)[:, 0], label="Wed")
positive_graph.plot(thu_time, np.array(thu_pos)[:, 0], label="Thu")
positive_graph.plot(fri_time, np.array(fri_pos)[:, 0], label="Fri")
positive_graph.plot(sat_time, np.array(sat_pos)[:, 0], label="Sat")
positive_graph.plot(sun_time, np.array(sun_pos)[:, 0], label="Sun")


plt.xlabel("Hour")
plt.ylabel("NA")
plt.title("Hourly changes in individual affect broken down by day of the week")


positive_graph.legend(loc='upper right', ncol = 7)


plt.show()

