import RPi.GPIO as GPIO
import time
from datetime import datetime
import json

GPIO.setmode(GPIO.BOARD)
LDR_PIN = 7

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
    while True:
        time.sleep(5)
        c = rc_time(LDR_PIN)
        status = {
            "occupied": c < 9999,
            "meeting": False,
            "last_updated": datetime.now().strftime("%I:%M:%S")
        }
        print(status)
        with open('status.json', 'w') as status_file:
            json.dump(status, status_file)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
