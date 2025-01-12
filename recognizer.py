import json
import uuid
from datetime import datetime
import cv2
from cv_utils import draw_text_top_right, draw_text_top_left
from container_number_check import is_valid_iso_container


class DictObject(object):
    def __init__(self, dict_):
        self.__dict__.update(dict_)

    @classmethod
    def from_dict(cls, d):
        return json.loads(json.dumps(d), object_hook=DictObject)

class Recognizer:
    def __init__(self, modelRecognition, recognitionStream):
        self.reset()
        self.lastRecognition = ""
        self.lastFailedRecognition = ""
        self.modelRecognition = modelRecognition
        self.recognitionStream = recognitionStream

    def reset(self):
        self.detectedCount = 0
        self.notDetectedCount = 0
#        self.lastRecognition = ""
#        self.lastFailedRecognition = ""
        self.recognitions = []

    def recognize(self):
        objectToRecognize = max(self.recognitions, key=lambda obj: obj.confidence)
        x1 = objectToRecognize.x1
        y1 = objectToRecognize.y1
        x2 = objectToRecognize.x2
        y2 = objectToRecognize.y2

        croppedRoi= objectToRecognize.frame[int(y1):int(y2), int(x1):int(x2)] 
        current_datetime = datetime.now()
        timestamp_string = current_datetime.strftime("%Y%m%d%H%M%S")
        filename = uuid.uuid4().hex+"_number_"+timestamp_string + ".jpg"
        cv2.imwrite(filename, croppedRoi)

        bestCandidate = recognize(croppedRoi, self.modelRecognition, self.recognitionStream, objectToRecognize.recogClass)
        if is_valid_iso_container(bestCandidate):
           self.lastRecognition = bestCandidate
        else:
            self.lastFailedRecognition = bestCandidate
        return

    def printLastRecogData(self):
        if self.lastFailedRecognition !="" or self.lastRecognition:
            print("OK: ", self.lastRecognition, " NOK: ", self.lastFailedRecognition)

    def transition(self, event):
        if event.name == "detected":
            self.detectedCount += 1
            self.recognitions.append(event)
        if event.name == "not_detected":
            self.notDetectedCount += 1

        if self.detectedCount > 2:
            self.recognize()
            self.reset()
        if self.notDetectedCount > 2:
            self.reset()
            self.lastRecognition = ""
            self.lastFailedRecognition = ""

        #print("Detected", self.detectedCount,  " Not detected:", self.notDetectedCount)

class Event:
    def __init__(self, name, recogClass, confidence, x1, y1, x2, y2, frame):
        self.name = name
        self.confidence = confidence
        self.recogClass = recogClass
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.frame = frame


def calculate_iou(recog1, recog2):
    x1_inter = max(recog1.box.x1,  recog2.box.x1)
    y1_inter = max(recog1.box.y1, recog2.box.y1)
    x2_inter = min(recog1.box.x2, recog2.box.x2)
    y2_inter = min(recog1.box.y2, recog2.box.y2)

    # Compute the area of intersection
    inter_width = max(0, x2_inter - x1_inter)
    inter_height = max(0, y2_inter - y1_inter)
    inter_area = inter_width * inter_height

    # Compute the area of each box
    box1_area = (recog1.box.x2 - recog1.box.x1) * (recog1.box.y2 - recog1.box.y1)
    box2_area = (recog2.box.x2 - recog2.box.x1) * (recog2.box.y2 - recog2.box.y1)

    # Compute the union area
    union_area = box1_area + box2_area - inter_area

    # Compute IoU
    iou = inter_area / union_area if union_area > 0 else 0
    return iou

def detect_overlapping_boxes(recog, iou_threshold=0.5):
    overlapping_pairs = dict()
    n = len(recog)

    for i in range(n):
         overlapping_pairs[i] = [recog[i]]
    for i in range(n):
        for j in range(i + 1, n):
            iou = calculate_iou(recog[i], recog[j])
            if iou > iou_threshold:
               #overlapping_pairs.append((recog[i], recog[j]))
               overlapping_pairs[i].append(recog[j])

    return overlapping_pairs

def recognize(croppedRoi, modelRecognition, outputVideoStream, direction='container_number_v'):
   results = modelRecognition.predict(croppedRoi, imgsz=640, line_width=1, show_conf=False, show_labels=True,verbose=False)
   names = modelRecognition.names
   annotated_frame = results[0].plot(line_width=1)
   outputVideoStream.set_frame(annotated_frame)

   resultSummarized = results[0].summary()

#   convertedResults = convertResult(results, names)
   if direction=='container_number_h':
      sorted_detections = DictObject.from_dict(sorted(resultSummarized, key=lambda d: d["box"]["x1"], reverse=False))
   elif direction=='container_number_v':
      sorted_detections = DictObject.from_dict(sorted(resultSummarized, key=lambda d: d["box"]["y1"], reverse=False))
#   printDetections(sorted_detections)
#   print("len:", len(sorted_detections), "json", json.dumps(sorted_detections, indent=2))
   else:
      return ""
   
   overlapping = detect_overlapping_boxes(sorted_detections)
   ret = []
   for key, value in overlapping.items():
      if len(value) == 1:
         ret.append(names[getattr(value[0], "class")])

   return "".join(ret).upper()
