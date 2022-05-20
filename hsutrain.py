import cv2
import numpy as np
from victim import *

i = 0

vid = cv2.VideoCapture(1)
while(True):
    _, frame = vid.read()
    letter_img, frame = get_letter_img(frame)
    
    cv2.imshow("frame", frame)
    cv2.imshow("letter", letter_img)
    
    if cv2.waitKey(1) & 0xFF == ord(' ') and len(letter_img) != 0:
        print("saving")
        cv2.imwrite("train/u.jpg", letter_img)
        i += 1
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
vid.release()
cv2.destroyAllWindows()
