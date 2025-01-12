import cv2
import uuid
import json
import imutils
from datetime import datetime
from ultralytics import YOLO
from mjpeg_streamer import MjpegServer, Stream
from container_number_check import is_valid_iso_container
from recognizer import Recognizer, Event
from cv_utils import draw_text_top_right, draw_text_top_left

def captureCam():
   cap = cv2.VideoCapture("/dev/v4l/by-id/usb-HD_USB_Camera_HD_USB_Camera-video-index0")
   cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
   cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
   return cap

def captureUrl(url):
   cap = cv2.VideoCapture(url)
   return cap

class DictObject(object):
    def __init__(self, dict_):
        self.__dict__.update(dict_)

    @classmethod
    def from_dict(cls, d):
        return json.loads(json.dumps(d), object_hook=DictObject)

# Load the YOLO model
#model = YOLO("detection_small3_ncnn_model")
#model = YOLO("detection_small6_ncnn_model") 
#model = YOLO("detection_small10_ncnn_model") # works best 
model = YOLO("detection_small13.pt") 
#modelRecognition = YOLO("numbers_big2_ncnn_model")
# modelRecognition = YOLO("numbers_small.pt")
##modelRecognition = YOLO("numbers_small5_ncnn_model")
#modelRecognition = YOLO("numbers_small8_ncnn_model")
modelRecognition = YOLO("numbers_small10.pt")

# Open the video file
cap = captureCam()
#cap = captureUrl("http://192.168.178.48:8082/")
#cap = captureUrl("http://192.168.178.48:8082/static")


#rotationDegree = 21
rotationDegree = 0
#startX = 530
startX = 0
#startY = 0
startY = 0

detectionStream = Stream("detection", size=(1280, 960), quality=50, fps=30)
recognitionStream = Stream("recognition", size=(640, 480), quality=50, fps=30)
server = MjpegServer("*", 8080)
server.add_stream(detectionStream)
server.add_stream(recognitionStream)
server.start()
recognizer = Recognizer(modelRecognition, recognitionStream)
# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        frame = imutils.rotate(frame, rotationDegree)
        frame = frame[startY:,startX:]
        # Run YOLO inference on the frame
        candidates = []
        candidatesNOK = []
        results = model(frame,imgsz=640,verbose=False, conf=0.6)
        summary = results[0].summary()
        if len(summary) <=0:
           event = Event("not_detected", "", 1, 0,0,0,0,0)
           recognizer.transition(event)
        for recog in summary:
           name = recog["name"]
           box = recog["box"]
           x1 = box["x1"]
           y1 = box["y1"]
           x2 = box["x2"]
           y2 = box["y2"]
           confidence = recog["confidence"]
           if name=="container_number_v" or name=="container_number_h":
              current_datetime = datetime.now()
              timestamp_string = current_datetime.strftime("%Y%m%d%H%M%S")
              filename = uuid.uuid4().hex+"_"+timestamp_string + ".jpg"
              cv2.imwrite(filename, frame)

              event = Event("detected", name, confidence, x1, y1, x2, y2, frame)
              recognizer.transition(event)
           else:
               print(name)
         #   print(name, x1,y1,x2,y2)
           # Crop the object using the bounding box coordinates
#           croppedRoi= frame[int(y1):int(y2), int(x1):int(x2)] 
#           bestCandidate = recognize(croppedRoi, modelRecognition,recognitionStream, name )
#           if is_valid_iso_container(bestCandidate):
#              print(bestCandidate)
#              candidates.append(bestCandidate)
#           else:
#              candidatesNOK.append("NOK: " + bestCandidate)
              

        
        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        #draw_text_top_right(annotated_frame, "OK " + "\n".join(candidates))
        draw_text_top_right(annotated_frame, "OK " + recognizer.lastRecognition, color=(0, 255, 0))
        #draw_text_top_left(annotated_frame, "NOK " + "\n".join(candidates))
        draw_text_top_left(annotated_frame, "NOK " + recognizer.lastFailedRecognition, color=(0,0,255))
        recognizer.printLastRecogData()
        # Display the annotated frame
        detectionStream.set_frame(annotated_frame)
#        filename = uuid.uuid4().hex+"_rec.jpg"
#        cv2.imwrite(filename, annotated_frame)
#        cv2.imshow("YOLO Inference", annotated_frame)
#         boxes = results[0].boxes.xyxy.tolist()
#         for i, box in enumerate(boxes):
#            print("box inner:", box)
#            x1, y1, x2, y2 = box
#            # Crop the object using the bounding box coordinates
#            croppedRoi= frame[int(y1):int(y2), int(x1):int(x2)]
#            # Save the cropped object as an image
#  #          cv2.imwrite('ultralytics_crop_' + str(i) + '.jpg', ultralytics_crop_object)
# #           cv2.imshow("cropped", croppedRoi)
#       #     recognize(croppedRoi, modelRecognition)
#         # Break the loop if 'q' is pressed
#        if cv2.waitKey(1) & 0xFF == ord("q"):
#            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()

