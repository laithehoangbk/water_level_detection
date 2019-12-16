import cv2 as cv
import numpy as np
import math

if __name__ == "__main__":
    
    original_img = cv.imread('img2.jpg')
    original_img = cv.pyrDown(original_img)
    cv.imshow('original_img', original_img)
    
    # blur_img = cv.blur(original_img, (3, 3))

    # Otsu's thresholding after Gaussian filtering
    gray = cv.cvtColor(original_img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (11, 11), 0)
    

    # th = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY,11,2)
    ret, th = cv.threshold(blur, 60, 255, cv.THRESH_BINARY)
    # ret, th = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    cv.imshow('th', th)


    # hsv_img = cv.cvtColor(blur_img, cv.COLOR_BGR2HSV)

    # gray = cv.cvtColor(blur_img, cv.COLOR_BGR2GRAY)
    # edges = cv.Canny(gray, 60, 120)
    # cv.imshow('edges', edges)

    cv.waitKey(0)