import cv2
from feat import Detector
from feat.utils.io import get_test_data_path
from feat.plotting import imshow

import json

detector = Detector(
    face_model="retinaface",
    landmark_model="mobilefacenet",
    au_model="xgb",
    emotion_model="resmasknet",
    facepose_model="img2pose",
)


# Helper to point to the test data folder
test_data_dir = get_test_data_path()


# Opens the inbuilt camera of laptop to capture video.
cap = cv2.VideoCapture(0)
i = 0

single_face_predictions = []

while(cap.isOpened()):
    ret, frame = cap.read()
      
    # This condition prevents from infinite looping 
    # incase video ends.
    if ret == False:
        break
      
    # Save Frame by Frame into disk using imwrite method
    fileName = "images" + "/" + "Frame"+str(i)+".jpg"
    cv2.imwrite(fileName, frame)

    #imshow (fileName)

    single_face_predictions.append (detector.detect_image(fileName))

    i += 1

    if (i == 10):
        break
  
cap.release()
cv2.destroyAllWindows()


output = []
for prediction in single_face_predictions:
    output.append(prediction.to_json ())


with open ("output.json", "w") as file:
    file.write (json.dumps (output, indent=4))


