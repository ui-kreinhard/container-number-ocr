import cv2
import sys
import time
from mjpeg_streamer import MjpegServer, Stream


imageStream = Stream("static", size=(1280, 960), quality=50, fps=30)
server = MjpegServer("*", 8082)
server.add_stream(imageStream)
server.start()
while True:
    frame = cv2.imread(sys.argv[1])
    imageStream.set_frame(frame)
    time.sleep(5)