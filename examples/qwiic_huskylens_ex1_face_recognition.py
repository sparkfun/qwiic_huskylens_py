#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_template_ex1_title.py TODO: replace template and title
#
# TODO: Add description for this example
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, TODO: month and year
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2024 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#===============================================================================

import qwiic_huskylens 
import sys
import time

learnedBlocks = {} # In the form of {id: name}

def printBlocks(device):
	myBlocks = device.blocks

	for i, block in enumerate(myBlocks):
		print("Block #{}".format(i))
		if block.id in learnedBlocks.keys():
			print("Block Name: " + learnedBlocks[block.id])
		print ("Block ID: " + str(block.id))
		print ("Block X: " + str(block.xCenter))
		print ("Block Y: " + str(block.yCenter))
		print ("Block Width: " + str(block.width))
		print ("Block Height: " + str(block.height))
		print("\n")

def runExample():
	print("\nQwiic Huskylens Example 1 - Face Recognition\n")

	# Create instance of device
	myDevice = qwiic_huskylens.QwiicHuskylens() 

	# Check if it's connected
	if myDevice.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection",
			file=sys.stderr)
		return

	# Initialize the device
	myDevice.begin()

	myDevice.request_forget()
	myDevice.request_algorithm(myDevice.kAlgorithmFaceRecognition)

	# Prompt user to learn the first face, and ask for the name
	print("Lets teach the HuskyLens the first face.")
	name = input("Enter the name of the face you are about to teach the lens: ")
	print("Please show the face to the camera.")

	# The device will return "blocks" when it sees a face while in face recognition mode
	while (len(myDevice.blocks) == 0):
		myDevice.request_blocks()

	# When the device sees a face, let's learn it!
	myDevice.request_learn()
	myDevice.name_last(name)
	learnedBlocks[1] = name # The first learned face will always have an ID of 1 and will increment from there
	print("Face learned!")

	# Prompt user to learn the second face, and ask for the name
	print("Lets teach the HuskyLens the second face.")
	name = input("Enter the name of the face you are about to teach the lens: ")
	print("Please show the face to the camera.")
	myDevice.request_blocks()
	while (len(myDevice.blocks) == 0):
		myDevice.request_blocks()

	myDevice.request_learn()
	myDevice.name_last(name)
	learnedBlocks[2] = name
	print("Face learned!")

	nScans = 0
	while True:
		myDevice.request_blocks()
		if len(myDevice.blocks) == 0:
			print("No blocks found")
		else:
			print("----------------------New Blocks Scan #{}----------------------".format(nScans))
			printBlocks(myDevice)
			nScans += 1

		time.sleep(2)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)