import RPi.GPIO as GPIO
import time

D = [26, 19, 13, 6, 5, 11, 9, 10]

GPIO.setmode(GPIO.BCM)
GPIO.setup(D, GPIO.OUT)

def num2dac(value):
    GPIO.output(D, [int(i) for i in bin(value)[2:].zfill(8)])
            
try:
    while True:
        x = (int(input('Vvedite chislo (-1 dlya vihoda):')))
        if x != -1:
            num2dac(x)
        else:
            break
finally:
    GPIO.output(D, 0)
    GPIO.cleanup()