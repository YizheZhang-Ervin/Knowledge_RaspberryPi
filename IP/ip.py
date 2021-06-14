import socket
import uuid
import time
import os
import logging
 
from logging import handlers
 
# 获取MAC地址
def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])
 
# 获取IP地址
def get_host_ip():
    try:
        my = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        my.connect(('8.8.8.8', 80))
        # ip = my.getsockname()[0]
        ipList = my.getsockname()
    finally:
        my.close()
    return ipList
 
def _logging(**kwargs):
    level = kwargs.pop('level', None)
    filename = kwargs.pop('filename', None)
    datefmt = kwargs.pop('datefmt', None)
    format = kwargs.pop('format', None)
    if level is None:
        level = logging.DEBUG
    if filename is None:
        filename = 'default.log'
    if datefmt is None:
        datefmt = '%Y-%m-%d %H:%M:%S'
    if format is None:
        format = '%(asctime)s [%(module)s] %(levelname)s [%(lineno)d] %(message)s'
 
    log = logging.getLogger(filename)
    format_str = logging.Formatter(format, datefmt)
    # backupCount 保存日志的数量，过期自动删除
    # when 按什么日期格式切分(这里方便测试使用的秒)
    th = handlers.TimedRotatingFileHandler(filename=filename, when='H', backupCount=3, encoding='utf-8')
    th.setFormatter(format_str)
    th.setLevel(logging.DEBUG)
 
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    #  ch.setFormatter(format)
    log.addHandler(ch)
 
    log.addHandler(th)
    log.setLevel(level)
    return log
 
os.makedirs("logs", exist_ok=True)
mylog = _logging(filename='logs/udpserver.log')
 
print("等待30秒")
mylog.debug("等待30秒")
time.sleep(30)
print("等待结束")
mylog.debug("等待结束")
 
HOST = ''
PORT = 9999
BUFSIZ = 1024
ADDRESS = (HOST, PORT)
 
udpServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpServerSocket.bind(ADDRESS)  # 绑定客户端口和地址
 
myname = socket.gethostname()
print("myname:" + myname)
mylog.debug("myname:" + myname)
myIPList = get_host_ip()
print("myIPList:" + str(myIPList))
mylog.debug("myIPList:" + str(myIPList))
macAddress = get_mac_address()
print("macAddress:" + macAddress)
mylog.debug("macAddress:" + macAddress)
 
while True:
    print("waiting for message...")
    mylog.debug("waiting for message...")
    data, addr = udpServerSocket.recvfrom(BUFSIZ)
    currCode = data.decode('utf-8')
    print("接收到数据：" +currCode)
    mylog.debug("接收到数据："+currCode)
 
    # content = '[%s] %s' % (bytes(ctime(), 'utf-8'), data.decode('utf-8'))
    # 发送服务器时间
    if currCode == "TIME":
        content = "Time:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        udpServerSocket.sendto(content.encode('utf-8'), addr)
    # 发送IP地址
    elif currCode == "IP":
        content = "IP:" + str(myIPList)
        udpServerSocket.sendto(content.encode('utf-8'), addr)
    # 发送mac地址
    elif currCode == "MAC":
        content = "MAC:" + macAddress
        udpServerSocket.sendto(content.encode('utf-8'), addr)
    # 发送ip mac地址
    elif currCode == "IP_MAC":
        content = "IP:" + str(myIPList) + "|MAC:" + macAddress
        udpServerSocket.sendto(content.encode('utf-8'), addr)
    # 退出UDP服务端
    elif currCode == "EXIT":
        content = "服务端退出"
        udpServerSocket.sendto(content.encode('utf-8'), addr)
        # print(content)
        break
    # 重启
    elif currCode == "REBOOT":
        content = "服务端重启"
        udpServerSocket.sendto(content.encode('utf-8'), addr)
        print("服务端开始重启")
        mylog.debug("服务端开始重启")
        os.system('shutdown -r now')
        break
    # 关机
    elif currCode == "SHUTDOWN":
        content = "服务端关机"
        udpServerSocket.sendto(content.encode('utf-8'), addr)
        print("服务端开始关机")
        mylog.debug("服务端开始关机")
        os.system('sudo shutdown -h now')
        break
    else:
        udpServerSocket.sendto("Bad Key".encode('utf-8'), addr)
 
    # content = '[%s] %s %s' % (bytes(ctime(), 'utf-8'), str(myIPList), macAddress)
    # udpServerSocket.sendto(content.encode('utf-8'), addr)
    print('...received from and returned to:', addr)
    mylog.debug('...received from and returned to:', addr)
udpServerSocket.close()
print("服务端退出")
mylog.debug('服务端退出')