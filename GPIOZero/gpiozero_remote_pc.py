# Windows/Linux远程控制gpio
from gpiozero import LED,Button,Buzzer,LEDBoard,MotionSensor,LightSensor,Robot
from gpiozero.tools import zip_values
from gpiozero.pins.pigpio import PiGPIOFactory
from sense_hat import SenseHat

# 按钮+发光二极管
factory = PiGPIOFactory(host='192.168.1.3')
button = Button(2)
led = LED(17,pin_factory=factory)
led.source = button

# 按钮 + 蜂鸣器
ips = ['192.168.1.3','192.168.1.4','192.168.1.5']
remotes = [PiGPIOFactory(host=ip) for ip in ips]
button = Button(17)
buzzers = [Buzzer(21,pin_factory=r) for r in remotes]
for buzzer in buzzers:
    buzzer.source = button

# 人体感应传感器 + 发光二极管
ips = ['192.168.1.3','192.168.1.4','192.168.1.5']
remotes = [PiGPIOFactory(host=ip) for ip in ips]
leds = LEDBoard(2,3,4,5)
sensors = [MotionSensor(17,pin_factory=r) for r in remotes]
leds.source = zip_values(*sensors)

# 光线传感器
remote_factory = PiGPIOFactory(host='192.168.1.3')
light = LightSensor(4,pin_factory=remote_factory)
sense = SenseHat()
blue = (0,0,255)
yellow = (255,255,0)
while True:
    if light.value>0.5:
        sense.clear(yellow)
    else:
        sense.clear(blue)

# 机器人
remote_factory = PiGPIOFactory(host='192.168.1.3')
robot = Robot(left=(4,14),right=(17,18),pin_factory=factory)
left = Button(26)
right = Button(16)
fw = Button(21)
bw = Button(20)
left.when_pressed = robot.left
left.when_released = robot.stop
right.when_pressed = robot.right
right.when_released = robot.stop
fw.when_pressed = robot.forward
fw.when_released = robot.stop
bw.when_pressed = robot.backward
bw.when_released = robot.stop