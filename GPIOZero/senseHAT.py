from sense_emu import senseHat
sense = senseHat()

# 发光二极管
sense.clear((255,0,0))  # 改变发光二极管颜色
sense.show_message("xx",text_colour=(255,255,0),back_colour=(0,0,255),scroll_speed=0.05)  # 输出信息

# 游戏操纵杆
sense.set_pixel()

# 电子罗盘
sense.set_rotation(0)
sense.get_compass()
