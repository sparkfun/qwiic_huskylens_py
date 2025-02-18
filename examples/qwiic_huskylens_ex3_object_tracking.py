#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_huskylens_ex3_object_tracking.py
#
# This example shows how to set the Huskylens up for object tracking.
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, February 2025
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

# Provide platform-dependent way to get current time in milliseconds
if hasattr(time, "monotonic_ns"):
	def millis():
		return time.monotonic_ns() // 1000000 # works in CircuitPython and Linux/Raspberry Pi
else:
	def millis():
		return time.time_ns() // 1000000 #only works in MicroPython
	
def runExample():
	print("\nQwiic Huskylens Example 3 - Object Tracking\n")

	# Create instance of device
	myHuskylens = qwiic_huskylens.QwiicHuskylens() 

	# Check if it's connected
	if myHuskylens.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection",
			file=sys.stderr)
		return

	# Initialize the device
	myHuskylens.begin()

	myHuskylens.request_forget() # Forget all the objects that the device has already learned
	myHuskylens.request_algorithm(myHuskylens.kAlgorithmObjectTracking) # The device has several algorithms, we want to use object tracking

	# Prompt user to learn the first object
	print("Lets teach the HuskyLens an object to track.")
	print("Place the object in front of the camera.")
	print("When the object is in view and in the square, enter anything to continue.")
	input()
	
	# When we've lined up with our object, let's learn it
	myHuskylens.learn_new()
	print("Object learned!")

	print("Continue moving The object around until the Huskylen can track it at different angles.")
	print("will train for 3 seconds")

	startTime = millis()
	while (millis() - startTime < 3000):
		# Wait for the device to see the object
		myHuskylens.request_blocks()
		while (len(myHuskylens.blocks) == 0):
			myHuskylens.request_blocks()

		# Learn the object at the new angle
		myHuskylens.learn_same()
		time.sleep(0.1)

	nScans = 0
	while True:
		myHuskylens.request_blocks()
		if len(myHuskylens.blocks) == 0:
			print("No blocks found")
		else:
			print("----------------------New Blocks Scan #{}----------------------".format(nScans))
			myblocks = myHuskylens.blocks # Each recognized block will be stored in a "block" object containing the block's information

			for i, block in enumerate(myblocks):
				print("object #{}".format(i))
				print ("object ID: " + str(block.id))
				print ("object X: " + str(block.xCenter))
				print ("object Y: " + str(block.yCenter))
				print ("object Width: " + str(block.width))
				print ("object Height: " + str(block.height))
				print("\n")

				nScans += 1

		time.sleep(2)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)