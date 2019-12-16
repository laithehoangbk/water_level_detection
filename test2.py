# import cv2 as cv
# import numpy as np
# from scipy.ndimage.filters import median_filter
# import math

# SENSITIVITY = 35 #Tham số điều chỉnh để xác định mức nước hiệu quả hơn, khoảng từ [40-70] 
# CUT_BORDER = 0.0

# def unsharp(image, sigma=2, strength=3.5):
 
#     # Median filtering
#     image_mf = median_filter(image, sigma)
 
#     # Calculate the Laplacian
#     lap = cv.Laplacian(image_mf, cv.CV_64F)
 
#     # Calculate the sharpened image
#     sharp = image-strength*lap
 
#     # Saturate the pixels in either direction
#     sharp[sharp>255] = 255
#     sharp[sharp<0] = 0
    
#     return sharp

# if __name__ == "__main__":
    
#     original_img = cv.imread('img/img_test_1.jpg')
#     original_img = cv.pyrDown(original_img)
#     # cv.imshow('original_img', original_img)

#     orig_img_h, orig_img_w, _ = original_img.shape

#     border = int(orig_img_w * CUT_BORDER)
#     cut_img = original_img[:, border:orig_img_w - border]
#     cv.imshow('cut_img', cut_img)

#     gray_img = cv.cvtColor(cut_img, cv.COLOR_BGR2GRAY)

#     # cv.Sobel()

#     blur_img = cv.GaussianBlur(gray_img, (7, 7), 0)
#     # cv.imshow('blur_img', blur_img)

#     # lap_img = cv.Laplacian(blur_img, -1, ksize=1)
#     # cv.imshow('unsharp_img', lap_img)
    
#     # kernel = np.ones((3,3), np.uint8) 
#     # erode_img = cv.erode(lap_img, kernel, iterations=1)
#     # ret, thresh_img = cv.threshold(erode_img,0,255,cv.THRESH_BINARY)
#     # cv.imshow('thresh_img', thresh_img)


#     #Lọc biên ảnh
#     edges = cv.Canny(blur_img, 40, 100)
#     cv.imshow('edges', edges)

#     # kernel = np.ones((7,7),np.float32)/49
#     kernel1 =  np.array([[-1, -1, -1],
#                         [2, 2, 2],
#                         [-1, -1, -1]])

#     kernel2 =  np.array([[-1, -2, -1],
#                         [0, 0, 0],
#                         [1, 2, 1]])

#     dst = cv.filter2D(edges, -1, kernel1)
#     cv.imshow('dst', dst)

#     lines = cv.HoughLines(dst, 1, np.pi / 180, SENSITIVITY)
#     pt_list = []
#     if lines is not None:
#         for i in range(0, len(lines)):
#             rho = lines[i][0][0]
#             theta = lines[i][0][1]
#             a = math.cos(theta)
#             b = math.sin(theta)
#             x0 = a * rho
#             y0 = b * rho
#             pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
#             pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
#             # print(pt1, pt2)
#             if np.abs(pt1[0] - pt2[0]) < 150:
#                 continue
#             if np.abs(pt1[1] - pt2[1]) > 150:
#                 continue
#             pt_list.append([pt1, pt2])

#             cv.line(cut_img, pt1, pt2, (0,0,255), 2, cv.LINE_AA)

#     # pt_array = np.asarray(pt_list)
#     # pt_idx = np.argmin(np.abs(pt_array[:, 0, 1] - pt_array[:, 1, 1]))

#     # cv.line(cut_img, pt_list[pt_idx][0], pt_list[pt_idx][1], (0,0,255), 2, cv.LINE_AA)

#     cv.imshow("output", cut_img)

#     cv.waitKey(0)



import cv2
import numpy as np

def nothing(x):
    pass

# Create a black image, a window
img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('R','image',0,255,nothing)
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)

# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    r = cv2.getTrackbarPos('R','image')
    g = cv2.getTrackbarPos('G','image')
    b = cv2.getTrackbarPos('B','image')
    s = cv2.getTrackbarPos(switch,'image')

    if s == 0:
        img[:] = 0
    else:
        img[:] = [b,g,r]
