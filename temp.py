#!/usr/bin/python3

import os
import sys
import time
import subprocess
import re
import argparse

os.system('clear')



def main():
	#parseArgs() function returns the parsed arguments in a dictionary
	args = parseArgs()
	#if the user specified a duration for the test, use that. Else use default 60 secs
	if(args.time):
		testDuration = args.time
	else:
		testDuration = 60 #duration of the test in seconds, it is aproximate since it doesn't account for delays, would have to implement async timer

	initTime = time.time()
	currentTime = time.time()
	elapsedTime = 0.0;

	while(elapsedTime <= testDuration):
		
		currentData = System.getCurrentData()

		render(currentData, args)
		System.writeData(currentData)

		currentTime = time.time()
		elapsedTime = currentTime - initTime
	
		if(args.verbose):
			print('\n#####################')
			print('temps: ',System.tempReadings, '\n')
			print('speeds: ',System.fanReadings, '\n')

		time.sleep(3)

	print('\ntest done, ran for: ', "{:.1f}".format(elapsedTime), 'seconds', '\n')

	printTempResults(System.tempReadings)
	print('\n------------------------------------\n')
	printFanResults(System.fanReadings)





def render(currentData, args):
	os.system('clear')
	print('Refreshing temperature every 3 seconds \n')

	print('CPU   :', currentData['cpuTemp'])
	print('Fan Speed   :',currentData['fanSpeed'])	
	if args.stress:
		print('stress true')
	
#gets the array with all of the logged readings and get min, max and averages them
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

#setup argparser and parse the arguments, return the arguments namespace.
def parseArgs():
	parser = argparse.ArgumentParser(description='Measure and benchmark your CPU temperature')
	parser.add_argument('-t','--time', type=int, help='Define how long the test should go on for in seconds, default is 60 seconds')
	parser.add_argument('-v','--verbose', action='store_true', help='Show the list of recorded readings of the current test')
	parser.add_argument('-s','--stress', action='store_true', help='Apply stress test to the CPU while the test is running')
	args = parser.parse_args()
	return args


class System:
	def __init__(self):
		pass

	tempReadings = []
	fanReadings = []

	def getRawData():
		#getting the output of the 'sensors' command 
		return str(subprocess.check_output('sensors'))

	def parseCpuTemp(rawData):
		#parsing out the CPU temperature using regex, output looks like: Core X:    +55.55°C
		pattern = re.compile(r'(?i)core...\s+\+(\d+\.\d)')
		match = pattern.search(rawData)
		#converting it into a float for further calculations
		return float(match.group(1))

	def parseFanSpeed(rawData):
		#pattern = re.compile(r'(?i)fan.+(\d+)')
		pattern = re.compile(r'(\d+) RPM')
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

