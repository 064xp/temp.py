#!/usr/bin/python3

import os
import time
import subprocess
import re

os.system('clear')



def main():

	testDuration = 5 #duration of the test in seconds, it is aproximate since it doesn't account for delays, would have to implement async timer
	initTime = time.time()
	currentTime = time.time()
	elapsedTime = 0.0;

	while(elapsedTime <= testDuration):
		
		currentData = System.getCurrentData()

		render(currentData)
		System.writeData(currentData)

		currentTime = time.time()
		elapsedTime = currentTime - initTime
	
		#debugging purposes
		print('#####################')
		print('temps: ',System.tempReadings)
		print('speeds: ',System.fanReadings)

		time.sleep(3)

	print('test done, ran for: ', elapsedTime, 'seconds')


def render(currentData):
	os.system('clear')
	print('Refreshing temperature every 2 seconds \n')

	print('CPU   :', currentData['cpuTemp'])
	print('Fan Speed   :',currentData['fanSpeed'])	
	

def writeCurrentData(currentData):
	#write the data
	System.writeData(currentData)
	
	

class System:
	def __init__(self):
		pass

	tempReadings = []
	fanReadings = []

	def getRawData():
		#getting the output of the 'sensors' command 
		return str(subprocess.check_output('sensors'))

	def parseCpuTemp(rawData):
		#parsing out the CPU temperature using regex, output looks like: CPU:    +55.55°C
		pattern = re.compile(r'CPU:\s+\+(\d+\.\d)')
		match = pattern.search(rawData)
		#converting it into a float for further calculations
		return float(match.group(1))

	def parseFanSpeed(rawData):
		pattern = re.compile(r'Processor Fan:\s+(\d+)')
		match = pattern.search(rawData)
		return int(match.group(1))

	def getCurrentData():
		#Returns a dictionary with the parsed data
		rawData = System.getRawData()
		currentData = {
			'cpuTemp': System.parseCpuTemp(rawData),
			'fanSpeed': System.parseFanSpeed(rawData)
		}
		return currentData

	def writeData(currentData):
		System.tempReadings.append(currentData['cpuTemp'])
		System.fanReadings.append(currentData['fanSpeed'])


class Timer:
	def __init__(self):
		pass

if __name__ == "__main__":
    main()

