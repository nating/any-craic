import RPi.GPIO as GPIO
import time
from datetime import datetime
import json

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
LDR_PIN = 7
GREEN_LED_PIN = 11
RED_LED_PIN = 12
BTN_PIN = 15

# Returns an integer representing the light sensed by the LDR
def rc_time (pin):

    # Set the pin as output low
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)

    # Change the pin back to input
    GPIO.setup(pin, GPIO.IN)

    # Count how long it takes for the pin to go high
    count = 0
    while(GPIO.input(pin) == GPIO.LOW and count < 9999):
        count += 1
    return count

## When script is interupted, cleanup correctly
try:
    meeting = False
    while True:
        time.sleep(5)
        c = rc_time(LDR_PIN)
        occupied = c < 9999
        if(not GPIO.input(BTN_PIN)):
            print("button pressed")
            meeting = not meeting
        if(not occupied):
            meeting = False
        status = {
            "occupied": occupied,
            "meeting": meeting,
            "last_updated": datetime.now().strftime("%I:%M:%S")
        }
        with open('status.json', 'w') as status_file:
            json.dump(status, status_file)
        GPIO.output(GREEN_LED_PIN, (occupied and not meeting))
        GPIO.output(RED_LED_PIN, (occupied and meeting))
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
