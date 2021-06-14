from picamera import PiCamera

# cmd中 raspistill -rot 180 -o xx.jpg
# sudo raspi-config

camera = PiCamera()
# 预览
camera.start_preview()
camera.stop_preview()
# 旋转
camera.rotation = 180
# 拍照
camera.capture('/home/pi/Desktop/image.jpg')
# 录像
camera.start_recording('/home/pi/Desktop/video.mp4')
camera.stop_recording()