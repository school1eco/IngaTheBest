import RPi.GPIO as GPIO
import time
import numpy as np
import matplotlib.pyplot as plt


leds = [21, 20, 16, 12, 7, 8, 25, 24]
dac = [26, 19, 13, 6, 5, 11, 9, 10]
troykaModule = 17
comparator = 4

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(leds + dac, GPIO.OUT)
GPIO.setup(comparator, GPIO.IN)
GPIO.setup(troykaModule, GPIO.OUT)

def num2pins(pins, value):
    GPIO.output(pins, [int(i) for i in bin(value)[2:].zfill(8)])

def adc():
    value = 0
    direction = 1
    for i in range (8):
        delta = 2 ** (8 - i - 1)
        value += delta * direction
        num2pins(dac, value)
        time.sleep(0.001)
        direction = -1 if (GPIO.input(comparator) ==0) else 1
    return value

while adc() > 0:
    GPIO.output(troykaModule,0)
    
try:
    t_st = time.time()
    listV = []
    listT = []
    GPIO.output(troykaModule,1)
    
    while adc() < 256:
        listT.append(time.time()-t_st)
        listV.append((adc()))
        print(adc())
        
    GPIO.output(troykaModule,0)
    
    while adc() > 1:
        listT.append(time.time() - t_st)
        listV.append(adc())
        print(adc())
        
    plt.plot(listT,listV, 'r.')
    plt.show()
    np.savetxt('data.txt', listV, fmt='%d')

finally:
    
    GPIO.output(troykaModule,0)
    GPIO.output(dac+leds,0)
    GPIO.output(comparator,0)
