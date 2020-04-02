from adafruit_circuitplayground import cp
import board
import time
import pulseio
import array

# create IR input, maximum of 100 bits.
pulseIn = pulseio.PulseIn(board.IR_RX, maxlen=100, idle_state=True)
# clears any artifacts
pulseIn.clear()
pulseIn.resume()

# creates IR output pulse
pwm = pulseio.PWMOut(board.IR_TX, frequency=38000, duty_cycle=2 ** 15)
pulseOut = pulseio.PulseOut(pwm)

# array for pulse, this is the same pulse output when button a is pressed
# inputs are compared against this same array
# array.array('H'', [x]) must be used for IR pulse arrays when using pulseio
# indented to multiple lines so its easier to see
pulseArrayFan = array.array('H', [1296, 377, 1289, 384, 464, 1219, 1296, 379,
    1287, 394, 464, 1226, 461, 1229, 458, 1233, 464, 1226, 462, 1229, 456, 1232,
    1293, 6922, 1294, 379, 1287, 385, 463, 1220, 1295, 379, 1287, 395, 464,
    1225, 461, 1229, 458, 1232, 465, 1225, 462, 1229, 457, 1231, 1294, 6904, 1291,
    382, 1295, 377, 461, 1221, 1294, 380, 1296, 385, 464, 1226, 460, 1230, 457,
    1233, 464, 1234, 453, 1229, 457, 1230, 1295, 6918, 1287, 386, 1291, 381, 457,
    1225, 1289, 385, 1292, 388, 460, 1230, 457, 1232, 465, 1225, 462, 1228, 458,
    1232, 465, 1222, 1293, 6905, 1290, 382, 1295, 377, 461, 1221, 1293, 387, 1290,
    384, 464, 1225, 461, 1229, 458, 1231, 466, 1224, 463, 1226, 460, 1228, 1286, 6920,
    1296, 377, 1289, 382, 466, 1216, 1288, 386, 1291, 390, 458, 1231, 456, 1233, 464,
    1226, 460, 1229, 458, 1232, 465, 1222, 1292, 6904, 1291, 382, 1295, 376, 462, 1220,
    1295, 379, 1286, 395, 464, 1225, 462, 1232, 454, 1232, 466, 1223, 463, 1227, 460,
    1228, 1286, 6925, 1291, 381, 1296, 376, 462, 1224, 1290, 380, 1286, 394, 465, 1225,
    462, 1227, 460, 1230, 456, 1234, 463, 1227, 460, 1227, 1287, 6964, 1294, 379, 1287,
    384, 464, 1219, 1296, 378, 1288, 392, 456, 1234, 463, 1227, 460, 1230, 457, 1232, 464,
    1226, 461, 1227, 1288])

def laskoFanInfrared():
    pulseIn.pause()  # pauses IR detection
    cp.red_led = True
    pulseOut.send(pulseArrayFan)  # sends IR pulse
    time.sleep(0.2)  # wait so pulses don't run together
    pulseIn.clear()  # clear detected pulses to remove partial artifacts
    cp.red_led = False
    pulseIn.resume()  # resumes IR detection

fanOn = False
maxTemp = 70
feature = True

while True:
    if cp.button_b:
        print("Button B Pressed!")
        if feature:
            feature = False
        else:
            feature = True
    while True and feature:
        if cp.touch_A4:
            maxTemp = 60
        if cp.touch_A5:
            maxTemp = 70
        if cp.touch_A6:
            maxTemp = 80
        cp.pixels.brightness = 0.3
        temp_f = int(cp.temperature * (9 / 5) + 32)
        print(temp_f, maxTemp)
        if temp_f >= maxTemp and not fanOn:
            print("It's", temp_f, ". Too hot! It's", maxTemp, ". Turning fan on now.")
            laskoFanInfrared()
            fanOn = True
            cp.pixels.fill((0, 30, 30))
        if temp_f < maxTemp and fanOn:
            print("Not too hot!")
            cp.pixels.fill((0, 0, 0))
            laskoFanInfrared()
            fanOn = False
        if cp.button_b:
            print("Turning off.")
            if fanOn:
                cp.pixels.fill((0, 0, 0))
                laskoFanInfrared()
                fanOn = False
            time.sleep(5)
            feature = False
            break
        time.sleep(0.5)
