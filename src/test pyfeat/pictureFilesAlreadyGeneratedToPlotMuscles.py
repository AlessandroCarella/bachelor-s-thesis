from feat import Detector

detector = Detector(
    face_model="retinaface",
    landmark_model="mobilefacenet",
    au_model="xgb",
    emotion_model="resmasknet",
    facepose_model="img2pose",
)
    
for i in range(0,10):
    fileName = "images" + "/" + "Frame"+str(i)+".jpg"
    figs = detector.detect_image(fileName).plot_detections(faces="aus", muscles=True)
    
    i = 1
    #actually only 1, accessible also with figs[0], at least on the actual test set
    #probably the list is for pics with more than one face
    for elem in figs: 
        elem.savefig (fileName + " muscles " + str (i) + ".jpg")
        i += 1