#!/usr/bin/python3

import os
import sys
import time
import subprocess
import re

os.system('clear')



def main():

	print(sys.argv)

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
		print('speeds: ',System.fanReadings, '\n')

		time.sleep(3)

	print('test done, ran for: ', "{:.1f}".format(elapsedTime), 'seconds', '\n')

	printTempResults(System.tempReadings)
	print('\n--------------------------------------------------------------\n')
	printFanResults(System.fanReadings)


def render(currentData):
	os.system('clear')
	print('Refreshing temperature every 3 seconds \n')

	print('CPU   :', currentData['cpuTemp'])
	print('Fan Speed   :',currentData['fanSpeed'])	
	

def calculateResults(resultsArray):
	maxReading = max(resultsArray)
	minReading = min(resultsArray)	
	average = float("{:.1f}".format(sum(resultsArray)/len(resultsArray)))
	return({'max': maxReading, 'min': minReading, 'average': average})

def printTempResults(tempArray):
	results = calculateResults(tempArray)
	print("Average CPU Temperature: ", results['average'])
	print("Max CPU Temperature: ", results['max'])
	print("Min CPU Temperature: ", results['min'])

def printFanResults(fanArray):
	results = calculateResults(fanArray)
	print("Average Fan Speed: ", results['average'])
	print("Max Fan Speed: ", results['max'])
	print("Min Fan Speed: ", results['min'])


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



if __name__ == "__main__":
    main()

