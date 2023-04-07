from feat import Detector
import json



detector = Detector(
    face_model="retinaface",
    landmark_model="mobilefacenet",
    au_model="xgb",
    emotion_model="resmasknet",
    facepose_model="img2pose",
)

output = []
for i in range(0, 10):
    x = detector.detect_image("images" + "/" + "Frame"+str(i)+".jpg")
    output.append (x.to_json())

with open ("output.json", "w") as file:
    file.write (json.dumps (output, indent=4))
