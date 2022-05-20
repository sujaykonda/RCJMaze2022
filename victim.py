import cv2
import numpy as np

# from https://jdhao.github.io/2019/02/23/crop_rotated_rectangle_opencv/
def adjust(img, rect):
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    
    width = int(rect[1][0])
    height = int(rect[1][1])

    src_pts = box.astype("float32")
    # coordinate of the points in box points after the rectangle has been
    # straightened
    dst_pts = np.array([[0, height-1],
                        [0, 0],
                        [width-1, 0],
                        [width-1, height-1]], dtype="float32")

    # the perspective transformation matrix
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)

    # directly warp the rotated rectangle to get the straightened rectangle
    warped = cv2.warpPerspective(img, M, (width, height))
    
    return warped

def get_letter_img(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        box = np.int0(cv2.boxPoints(rect))
        cv2.drawContours(img,[box], 0, (0, 0, 255), 2)
        if(rect[1][0] * rect[1][1] > 10000):
            adjusted = adjust(gray, rect)
            adjusted = cv2.resize(adjusted, (50, 50))
            adjusted = cv2.cvtColor(adjusted, cv2.COLOR_GRAY2BGR)
            return adjusted, img
    return [], img