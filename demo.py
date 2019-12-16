import cv2 as cv
import numpy as np
import math

import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
IMAGES_MASK = config.get("path", "images_mask")
SOURCE_IMAGES_PATH = config.get("path", "source_dir")
RESULT_IMAGES_PATH = config.get("path", "result_dir")
# CUT_BORDER = config.getfloat("geometry", "cut_border")
# PRE_ROI_WIDTH = config.getfloat("geometry", "pre_roi_width")
# ROI_WIDTH = config.getfloat("geometry", "roi_width")
CUT_BORDER = 0.15
PRE_ROI_WIDTH = 0.15
ROI_WIDTH = 0.2

def get_roi(img, left_border, right_border):
   img_h, img_w, _ = img.shape
   left_part = img[:, 0:left_border]
   right_part = img[:, right_border:img_w]
   return np.column_stack((left_part, right_part))

def find_background(img, roi):
   img_h, img_w, _ = img.shape
   hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
   hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
   roi_hist = cv.calcHist([hsv_roi], [0, 1], None, [180, 256], [0, 180, 0, 256])
   mask = cv.calcBackProject([hsv_img], [0, 1], roi_hist, [0, 180, 0, 256], 1)
#    ksize = int(0.0025 * img_h)
#    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (ksize, ksize))
#    mask = cv.filter2D(mask, -1, kernel)
#    _, mask = cv.threshold(mask, 180, 255, cv.THRESH_BINARY)
   return mask

if __name__ == "__main__":

    original_img = cv.imread('6.jpg')
    original_img = cv.pyrDown(original_img)
    original_img = cv.GaussianBlur(original_img, (13,13), 1)
    
   #  original_img = cv.cvtColor(original_img, cv.COLOR_BGR2RGB)
    orig_img_h, orig_img_w, _ = original_img.shape
    cv.imshow('original_img', original_img)

    border = int(orig_img_w * CUT_BORDER)
    image = original_img[:, border:orig_img_w - border]
    image_h, image_w, _ = image.shape
    cv.imshow('image', image)

    pre_roi = get_roi(image, int(image_w * PRE_ROI_WIDTH), int(image_w - image_w * PRE_ROI_WIDTH))
    pre_mask = cv.bitwise_not(find_background(image, pre_roi))

    cv.imshow('pre_roi', pre_roi)

    cv.imshow('pre_mask', pre_mask)

    cv.waitKey(0)


    








    
   