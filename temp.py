#!/usr/bin/python3

import os
import time
import subprocess
import re
import argparse
from threading import Timer
from multiprocessing import Process, Event

os.system('clear')

refreshRate = 1
testDuration = 60

def main():
	#parseArgs() function returns the parsed arguments in a dictionary
	args = parseArgs()
	timerOverEvent = Event()
	timerOverEvent.set()

	if(args.time):
	#if the user specified a duration for the test, use that. Else use default 60 secs
		global testDuration
		testDuration = args.time

	if(args.stress):
		#if the stress test flag is set, initialize the load processes
		initLoads(timerOverEvent)

	timer = Timer(testDuration, stop, args=(timerOverEvent,))
	timer.start()

	#for getting elapsed time
	initTime = time.time()
	currentTime = time.time()
	elapsedTime = 0.0;

	while(timerOverEvent.is_set()):
		currentData = System.getCurrentData()

		render(currentData, elapsedTime, args)
		System.writeData(currentData)

		currentTime = time.time()
		elapsedTime = currentTime - initTime
	
		if(args.verbose):
			print('\n#####################')
			print('temps: ',System.tempReadings, '\n')
			print('speeds: ',System.fanReadings, '\n')

		time.sleep(refreshRate)

	timer.join()

	print('\ntest done, ran for: ', "{:.1f}".format(elapsedTime), 'seconds', '\n')

	printTempResults(System.tempReadings)
	print('\n------------------------------------\n')
	printFanResults(System.fanReadings)



def stop(event):
	event.clear()
	print('stop')

def render(currentData, elapsedTime, args):
	os.system('clear')
	print(f'Refreshing temperature every {refreshRate} seconds.')
	print(f'Test running for {testDuration} seconds. \n')

	print('CPU   :', currentData['cpuTemp'])
	print('Fan Speed   :',currentData['fanSpeed'])	
	if args.stress:
		print('\nStress test enabled, applying load to CPU...')
	print(f'\n\nElapsed Time: {round(elapsedTime)}s')
	
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

def initLoads(event):
	#Spawn a new process to run a Load for each core on the machine
	procs = []

	for i in range(os.cpu_count()):
		procs.append(Process(target=Load, args=(event,)))
	
	#start each process
	for process in procs:
		process.start()

def Load(event):
	#function to add a load to the cpu
	import hashlib	

	hashStr = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean vestibulum nec purus sit amet finibus. Sed consequat ornare pretium. Etiam posuere velit libero, et tristique velit sollicitudin eget."
	print('Applying load on CPU...')

	while event.is_set():
		hashStr = hashlib.sha256(hashStr.encode(encoding='UTF-8')).hexdigest()

if __name__ == "__main__":
    main()

