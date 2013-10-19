"""
gpioRap - A wrapper class for the RPi.GPIO module
Author - Martin O'Hanlon
Website - www.stuffaboutcode.com
"""

import RPi.GPIO as GPIO
import time

class GpioRap:
	"A wrapper class for the RPi.GPIO module"
	def __init__(self, gpioSetMode=None):
		"Constructor can be passed the gpio set mode, GPIO.BCM / GPIO.Board, if None is passed GPIO.BCM is default"
		#set default mode to BCM if None is passed
		if gpioSetMode == None: self.gpioSetMode = GPIO.BCM
		else: self.gpioSetMode = gpioSetMode
		GPIO.setmode(self.gpioSetMode)

	def createButton(self, gpioPin, pressedState):
		"Creates a button, gpioPin is the pin where the button is connected, pressedState is a boolean (True, False) which represents the value at the GPIO when the button is pressed"
  		return self.Button(gpioPin, pressedState)
	
	def createLED(self, gpioPin):
		"Creates an LED, gpioPin is the pin which is LED is connected to"
		return self.LED(gpioPin)
	
	def cleanup(self):
		"Cleans up the GPIO, in effect resetting all values to default and closes"
		#cleanup GPIO
		GPIO.cleanup()
	
	class Button:
		"A wrapper class for managing a single button"
		def __init__(self, gpioPin, pressedState):
			"Constructor must be passed gpioPin (the pin where the button is connected) and pressedState (a boolean [True, False] which represents the value at the GPIO when the button is pressed"
			self.gpioPin = gpioPin
			self.pressedState = pressedState
			# setup gpio pin as input
			GPIO.setup(self.gpioPin, GPIO.IN)
		
		def get(self):
			"Gets the current value of the gpio"
			return GPIO.input(self.gpioPin)

		def pressed(self):
			"Returns a boolean representing whether the button is pressed"
			buttonPressed = False
			# if gpio input is equal to the pressed state
			if GPIO.input(self.gpioPin) == self.pressedState:
				buttonPressed = True
			return buttonPressed

		def waitForPress(self, timeOut=None):
			"Waits for the button to be pressed (or an optional time out expires) and returns for a boolean representing whether the button is pressed"
			
			buttonPressed = False
			timedOut = False
			timeStarted = time.time()
			# if the button is pressed when the wait starts, wait till it is released
			while self.pressed() == True: time.sleep(0.01)
			
			# wait for the button to be pressed
			while buttonPressed == False and timedOut == False:
				buttonPressed = self.pressed()
				if timeOut != None:
					if (time.time() - timeStarted) > timeOut: timedOut = True
				time.sleep(0.01)

			return buttonPressed

	class LED:
		"A wrapper class for managing an LED"
		def __init__(self, gpioPin):
			"Constructor must be bassed gpioPin (the pin where the LED is connected)"
			self.gpioPin = gpioPin
			# setup gpio pin as output
			GPIO.setup(self.gpioPin, GPIO.OUT)
			self.off()

		def set(self, ledValue):
			"Sets the value of the LED [True / False]"
			self.ledValue = ledValue
			GPIO.output(self.gpioPin, self.ledValue)

		def get(self):
			"Gets the value of the led"
			return self.ledValue

		def on(self):
			"Turns the LED on"
			self.set(True)

		def off(self):
			"Turns the LED off"
			self.set(False)
			
		def toggle(self):
			"Toggles the LED, if its on, turns it off and vice versa"
			if self.ledValue == True: self.off()
			else: self.on()

		def flash(self, times, delay):
			"Flashes the LED, a number of times with a delay (in seconds) inbetween"
			for i in range(1, times):
				self.toggle()
				time.sleep(delay)


