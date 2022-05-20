import cv2
import numpy as np
from victim import *

trainData = np.array([cv2.imread("train/h.jpg").flatten(), cv2.imread("train/s.jpg").flatten(), cv2.imread("train/u.jpg").flatten()]).astype(np.float32)
responses = np.array([[1], [2], [3]]).astype(np.float32)
print(trainData.shape, responses.shape)

knn = cv2.ml.KNearest_create()
knn.train(trainData, cv2.ml.ROW_SAMPLE, responses)

left = cv2.VideoCapture(1)
right = cv2.VideoCapture(-1)
while(True):
    _, lframe = left.read()
    _, rframe = right.read()
    
    lletter, lframe = get_letter_img(lframe)
    rletter, rframe = get_letter_img(rframe)
    
    if(len(lletter) != 0):
        inp = np.array([lletter.flatten()]).astype(np.float32)
        print(inp.shape)
        _, result, _, dist = knn.findNearest(inp, 1)
        print("left")
        print(result, dist)
    if(len(rletter) != 0):
        inp = np.array([rletter.flatten()]).astype(np.float32)
        _, result, _, dist = knn.findNearest(inp, 1)
        print("right")
        print(result, dist)
    
    cv2.imshow("lframe", lframe)
    cv2.imshow("rframe", rframe)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
left.release()
right.release()
cv2.destroyAllWindows()