from typing import Counter
from bluedot import BlueDot
from gpiozero import LED,PWMLED,Robot

# 控制发光二极管
bd = BlueDot()
bd.color = 'red'
bd.square = True
led = LED(17)

flag = True
while flag:
    bd.wait_for_press()
    led.on()
    bd.wait_for_release()
    led.off()

# 调节器开关
def set_brightness(pos):
    brightness = (pos.y+1)/2
    led.value = brightness
led = PWMLED(27)
bd = BlueDot()
bd.when_moved = set_brightness

# 调舵机角度/马达速度
def swiped(swipe):
    swipe.speed
    swipe.angle
    swipe.distance
bd = BlueDot()
bd.when_swiped = swiped

# 旋转调节
count = 0
def rotated(rotation):
    global count
    count += rotation.value
    rotation.clockwise
bd = BlueDot()
bd.when_rotated = rotated
bd.rotation_segments = 16

# 机器人移动
bd = BlueDot()
robot = Robot(left=(4,14),right=(17,18))
def move(pos):
    if pos.top:
        robot.forward(pos.distance)
    elif pos.bottom:
        robot.backward(pos.distance)
    elif pos.left:
        robot.left(pos.distance)
    elif pos.right:
        robot.right(pos.distance)
bd.when_pressed = move  # 蓝点按下
bd.when_moved = move    # 蓝点移动
bd.when_released = robot.stop

# 机器人移动: 蓝点离中心越远，电机转速越大
def pos_to_value(x,y):
    left = y if x>0 else y+x
    right = y if x<0 else y-x
    return (clamped(left),clamped(right))

def clamped(v):
    return max(-1,min(1,v))

def drive():
    while True:
        if bd.is_pressed:
            x,y = bd.position.x,bd.position.y
            yield pos_to_values(x,y)
        else:
            yield (0,0)
robot = Robot(left=(4,14),right=(17,18))
bd = BlueDot()
robot.source = drive()