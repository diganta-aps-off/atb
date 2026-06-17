import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Ultrasonic pins
TRIG = 4
ECHO = 17

# Motor Driver Pins
ENA = 18
IN1 = 23
IN2 = 24

ENB = 19
IN3 = 27
IN4 = 22

# Setup
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

for pin in [ENA, IN1, IN2, ENB, IN3, IN4]:
    GPIO.setup(pin, GPIO.OUT)

# PWM for motor speed
pwmA = GPIO.PWM(ENA, 1000)
pwmB = GPIO.PWM(ENB, 1000)

pwmA.start(100)   # Full speed
pwmB.start(100)

def forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)

    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def distance():
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_timeout = time.time()

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if time.time() - start_timeout > 0.05:
            return 999

    end_timeout = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if time.time() - end_timeout > 0.05:
            return 999

    pulse_duration = pulse_end - pulse_start
    dist = pulse_duration * 17150

    return round(dist, 2)

try:
    while True:
        d = distance()

        print(f"Distance: {d} cm")

        if d <= 5:
            stop()
            print("Obstacle detected! Motors stopped.")
        else:
            forward()

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopping...")

finally:
    stop()
    pwmA.stop()
    pwmB.stop()
    GPIO.cleanup()