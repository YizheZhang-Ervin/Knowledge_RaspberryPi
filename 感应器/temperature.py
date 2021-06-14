#打开温度传感器文件
tfile = open("/sys/bus/w1/devices/28-00000494cb79/w1_slave")
#读取文件所有内容
text = tfile.read()
#关闭文件
tfile.close()
#用换行符分割字符串成数组，并取第二行
secondline = text.split("\n")[1]
#用空格分割字符串成数组，并取最后一个，即t=23000
temperaturedata = secondline.split(" ")[9]
#取t=后面的数值，并转换为浮点型
temperature = float(temperaturedata[2:])
#转换单位为摄氏度
temperature = temperature / 1000
#打印值
print(temperature)