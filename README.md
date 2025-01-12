# container-number-ocr

It's a weekend/holiday project aimed to train a yolov11 network for detecting and recognizing container numbers. Inspired by the benchmarks in https://docs.ultralytics.com/guides/raspberry-pi/ I thought to use it on a pi5 to recognize container numbers. 

In the first step it tries to identify region which are container numbers. In the second step the additional network tries to identify the single characters. There's no ocr engine integrated - the second network uses classes like 0,1,2,...A, B, C for recognitio and it's also a trained yolov11 network.

detection_small10.pt is the detection network. numbers_small11.pt is the network for recognizing the single characters with classes like 0,1,2,...A,B,C

# How to run

0. Read the code of detect_recognize.py and customize it to fit your input source (lol :))
1. Create venv and activate it
2. pip install ultralytics mjpeg_streamer imutils
3. python detect_recognize.py

NOTE: You can also run it on a rpi5 when exporting to ncnn with acceptable frame rates with ~5fps(not measured exactly). See https://docs.ultralytics.com/guides/raspberry-pi/
NOTE2: It's not a plug and play - it's a proof of concept.