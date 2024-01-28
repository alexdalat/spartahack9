#!/usr/bin/env python
import RPi.GPIO as GPIO          
import time

in1 = 24
in2 = 23
ena = 25
in3 = 27
in4 = 17
enb = 22
temp1 = 1

GPIO.setmode(GPIO.BCM)

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
pwma=GPIO.PWM(ena,1000)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
pwmb=GPIO.PWM(enb,1000)

# duty cycle
pwma.start(69) # 40 left for now
pwmb.start(40) # 69 right for now

print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")

def forward(duration):
    print("forward")
    start_time = time.time()
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    pwma.ChangeDutyCycle(69)
    pwmb.ChangeDutyCycle(40)
    while (1):
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            break

def reverse(duration):
    print("backward")
    start_time = time.time()
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in4,GPIO.HIGH)
    pwma.ChangeDutyCycle(69)
    pwmb.ChangeDutyCycle(40)
    while (1):
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            break

def left(duration):
    print("left")
    start_time = time.time()
    pwma.ChangeDutyCycle(0)
    pwmb.ChangeDutyCycle(100)
    while (1):
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            break
    pwma.ChangeDutyCycle(69)
    pwmb.ChangeDutyCycle(40)

def right(duration):
    print("right")
    start_time = time.time()
    pwma.ChangeDutyCycle(80)
    pwmb.ChangeDutyCycle(0)
    while (1):
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            break
    pwma.ChangeDutyCycle(69)
    pwmb.ChangeDutyCycle(40)

def stop(duration):
    print("stop")
    start_time = time.time()
    pwma.ChangeDutyCycle(0)
    pwmb.ChangeDutyCycle(0)
    while (1):
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            break

def main():

    while (1):
        
        user_input = input()
        
        if user_input == 'r':
            print("run!")
            
            forward(5)
            stop(1)
            right(1.5)
            stop(1)
            forward(2)
            stop(1)
            
            GPIO.cleanup()
            break

        else:
            print("bro...")
            print("please enter the defined data to continue.....")

if __name__ == "__main__":
    main()
