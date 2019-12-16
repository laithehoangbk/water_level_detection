import cv2 as cv
import numpy as np
import math

if __name__ == "__main__":
    
    cap = cv.VideoCapture(0)
    while(True):
        ret, original_img = cap.read()
        cv.imshow('show', original_img)
        if cv.waitKey(1) & 0xff == ord('q'):
            break

    cv.destroyAllWindows()