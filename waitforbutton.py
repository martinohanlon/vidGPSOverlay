import gpioRap as gpioRap
import RPi.GPIO as GPIO

#Create GpioRap class using BCM pin numbers
gpioRapper = gpioRap.GpioRap(GPIO.BCM)

#Create an LED, which should be attached to pin 17
led = gpioRapper.createLED(17)
#Create a button, which should be monitored by pin 4, where a False is read when the button is pressed
button = gpioRapper.createButton(4, False)

#Turn the led on
led.on()

buttonPressed = False

#Loop until exception (ctrl c)
while buttonPressed == False:
    #Wait for the button to be pressed
    if button.waitForPress(3) == True:
        buttonPressed = True

#turn led off
led.off()

#Cleanup
gpioRapper.cleanup()
