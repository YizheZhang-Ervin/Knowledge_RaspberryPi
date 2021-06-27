from gpiozero import LED,Button,TrafficLights,Buzzer
from gpiozero import PWMLED,LEDBoard,LEDBarGraph,RGBLED
from gpiozero import TonalBuzzer,DistanceSensor
from gpiozero import Motor,Robot,Servo,AngularServo
from gpiozero import DigitalOutputDevice,DigitalInputDevice,MotionSensor
from gpiozero import LightSensor,MCP3008, PingServer, StatusZero
from gpiozero import CPUTemperature, Energenie, TimeOfDay
from gpiozero.tones import Tone
from gpiozero.tools import zip_values,scaled,negated
from evdev import InputDevice,list_devices,ecodes
from time import sleep
from datetime import time
from signal import pause
import curses
from subprocess import check_call

# LED灯
led = LED(25) # 使用GP25
led.on() # 点亮
led.off() # 熄灭
sleep(1) # 等待1s
led.blink(on_time=5,off_time=2,n=2,background=True) # 闪烁
led.toggle()  # 转换功能
led.is_lit()  # 判断是否点亮
pause()

# 脉冲宽度调制LED
led2 = PWMLED(17)
led.value = 0
led.value = 0.5
led.value = 1
led.pulse()  # 淡入淡出(高->低->高->低)

# 全彩LED
led3 = RGBLED(red=9,green=10,blue=11)
led3.red = 1 # 全红
led3.red = 0.5 # 半红
led3.color = (1,0,1)  # 洋红
led3.color = (0,0,0)  # 关闭

# led板
leds = LEDBoard(5,6,13,19,26,pwm=True)
leds[0].on() # 开一个
leds.on()  # 全开
leds.off() # 全关
leds.value = (0.2,0,0.8,0,1)  # 指定哪些开关
leds.blink() # 全闪烁

# led灯条
graph = LEDBarGraph(5,6,13,19,26,20,pwm=True)
graph.value = 1/2 # 0全灭、-1全亮、-1/2左灭右亮、1/2左亮右灭

# 按钮
led = LED(16)
button = Button(2)
button.is_pressed  # 是否按下
button.wait_for_press() # 按下后才继续执行
button.when_pressed = led.on # 按下按钮
button.when_released = led.off # 松开按钮
button.pin.number # 按钮的针脚

# 红绿灯
lights = TrafficLights(25,7,8) # 红，绿，黄
lights.green.on()
lights.green.off()
lights.amber.on()
lights.amber.off()
lights.red.on()
lights.red.off()

# 有源蜂鸣器
bz = Buzzer(15)
bz.toggle()
bz.beep(on_time=1,off_time=2,n=2,backgroung=True)

# 无源蜂鸣器
b = TonalBuzzer(17)
b.play(Tone('A4'))
b.play(Tone(220.0))  # Hz
b.play(Tone(60)) # MIDI notation middle C
b.play('A4')
b.play(220.0)
b.play(60)

# 距离传感器
led = LED(16)
sensor = DistanceSensor(23,24,max_distance=1,threshold_distance=0.2)
sensor.distance
sensor.when_in_range = led.on
sensor.when_out_of_range = led.off

# 可变电阻器+模数转换器MCP3008 -> 调节发光二极管条
graph2 = LEDBarGraph(5,6,13,19,26,20,pwm=True)
pot = MCP3008(channel=0)
graph2.source = pot

# 可变电阻器+模数转换器MCP3008 -> 调节全彩LED
led4 = RGBLED(red=2,green=3,blue=4)
red_pot = MCP3008(channel=0)
green_pot = MCP3008(channel=1)
blue_pot = MCP3008(channel=2)
led.red = red_pot.value
led.green = green_pot.value
led.blue = blue_pot.value
# 上面三行可使用源引用方法: led.source = zip_values(red_pot,green_pot,blue_pot)

# 马达
motor = Motor(forward=4,backward=14)
motor.forward()
motor.backward()

# 机器人+传感器
robot = Robot(left=(4,14),right=(17,18))  # 左轮右轮
sensor2 = DistanceSensor(23,24,max_distance=1,threshold_distance=0.2)
sensor2.distance
sensor2.when_in_range = robot.backward
sensor2.when_out_of_range = robot.stop

# 机器人+按钮
robot = Robot(left=(4,14),right=(17,18))  # 左轮右轮
left = Button(26)
right = Button(16)
fw = Button(21)
bw = Button(20)
fw.when_pressed = robot.forward
fw.when_released = robot.stop
left.when_pressed = robot.left
left.when_released = robot.stop
right.when_pressed = robot.right
right.when_released = robot.stop
bw.when_pressed = robot.backward
bw.when_released = robot.stop

# 机器人+键盘 (curses命令行)
key = window.getch()
if key==curses.KEY_UP:
    robot.forward
elif key==curses.KEY_DOWN: 
    robot.backward
elif key==curses.KEY_LEFT: 
    robot.left
elif key==curses.KEY_RIGHT: 
    robot.right

# 机器人+键盘(evdev IDLE)
devices = [InputDevice(device) for device in list_devices()]
ecodes.EV_KEY
ecodes.KEY_UP
ecodes.KEY_DOWN
ecodes.KEY_LEFT
ecodes.KEY_RIGHT

# 调机器人马达速度
robot = Robot(left=(4,14),right=(17,18))  # 左轮右轮
left_pot = MCP3008(0)
right_pot = MCP3008(1)
robot.source = zip(scaled(left_pot,-1,1),scaled(right_pot,-1,1))

# 舵机(数字信号)
servo = Servo(17)
servo.min()
servo.mid()
servo.max()

# 舵机(模拟信号)
s = AngularServo(17,min_angle=-42,max_angle=44)
s.angle

# 继电器
relay = DigitalOutputDevice(17)
relay.on()
relay.off()

# 霍尔传感器
hallsensor = DigitalInputDevice(17)
if hallsensor:
    print("高电平")
else:
    print("低电平")

# 力学传感器:开关/体重/加速计/陀螺仪
## 开关关机
def shutdown():
    check_call(['sudo','poweroff'])
button = Button(17,hold_time=2)
button.when_held = shutdown

# 热学传感器
## 机器人+人体感应器
pir = MotionSensor(4)
robot = Robot(left=(4,14),right=(17,18))  # 左轮右轮
pir.when_motion = robot.forward
pir.when_no_motion = robot.stop
# 或用 robot.source = zip_values(pir,pir)

## 温度传感器
def convert(gen):
    for v in gen:
        yield (v*3.3-0.5)*100
adc = MCP3008(channel=0)
for temp in convert(adc.values):
    print(temp)

# 红外传感器
## 光敏传感器
sensor = LightSensor(18)
led = LED(16)
sensor.wait_for_light()
sensor.wait_for_dark()
sensor.when_dark = led.on
sensor.when_light = led.off
# 或 led = PWMLED(16)  led.source=sensor

## 循迹传感器

# 检查网络是否连通
green = LED(17)
red = LED(18)
baidu = PingServer('www.baidu.com')
green.source = baidu
green.source_delay = 60
red.source = negated(green)

# 判断是否在线
status = StatusZero("A","B","C")
statuses = {
    PingServer("xxx"):status.A,
    PingServer("yyy"):status.B,
    PingServer("zzz"):status.C,
}
for server,leds in statuses.items():
    leds.green.source = server
    leds.green.source_delay = 60
    leds.red.source = negated(leds.green)
    
# CPU温度
cpu = CPUTemperature(min_temp=50,max_temp=90)
leds = LEDBarGraph(2,3,4,5,6,7,8,pwm=True)
leds.source = cpu

# 通电断电
lamp = Energenie(1)
daytime = TimeOfDay(time(8),time(20))
lamp.source = daytime
lamp.source_delay = 60