import cv2 as cv
import numpy as np
import math
import time

SENSITIVITY = 25 #Tham số điều chỉnh để xác định mức nước hiệu quả hơn, khoảng từ [40-70] 
THRESH_VAL = 80
CUT_BORDER = 0.25
COLOR_VAL = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
def on_trackbar(val):
    pass

def fildHoughLines(image, sens = 40, x = 0, minLine = 20, maxLine = 50):
    lines = cv.HoughLinesP(image, 1, np.pi / 180, sens, None, minLine, maxLine)
    pt0_list = []
    if lines is not None:
        for i in range(0, len(lines)):
            l = lines[i][0]
            pt1 = (l[0], l[1])
            pt2 = (l[2], l[3])

            if (x == 0):
                if np.abs(pt1[0] - pt2[0]) < 20:
                    continue
                if np.abs(pt1[1] - pt2[1]) > 20:
                    continue
                # cv.line(draw_cut_img, pt1, pt2, (255, 0, 255), 1, cv.LINE_AA) 
                pt0 = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2) 
                if pt0[0] >= 1 and pt0[1] <= image.shape[0] - 15:
                    # cv.circle(draw_cut_img, pt0, 1, (255, 127, 0), 2)
                    pt0_list.append(pt0)
            else:
                if np.abs(pt1[0] - pt2[0]) > 20:
                    continue
                if np.abs(pt1[1] - pt2[1]) < 20:
                    continue
                # cv.line(draw_cut_img, pt1, pt2, (255, 127, 127), 1, cv.LINE_AA) 
                pt0 = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2) 
                # cv.circle(draw_cut_img, pt0, 2, (0, 127, 255), 2)
                pt0_list.append(pt0)

    return pt0_list


if __name__ == "__main__":
    cv.namedWindow("output", cv.WINDOW_AUTOSIZE)
    cv.createTrackbar('sensitivity', 'output', SENSITIVITY, 40, on_trackbar)
    cv.createTrackbar('sensitivity_bottle', 'output', 90, 200, on_trackbar)
    cv.createTrackbar('min', 'output', 100, 250, on_trackbar)
    cv.createTrackbar('max', 'output', 150, 250, on_trackbar)
    cv.createTrackbar('cap thresh', 'output', THRESH_VAL, 255, on_trackbar)
    
    cap = cv.VideoCapture(0)
    while(True):
        start = time.time()
        # Đọc ảnh đầu vào
        # original_img = cv.imread('img2/4.jpg')
        ret, original_img = cap.read()

        # Giảm kích thước ảnh 2 lần
        # original_img = cv.pyrDown(original_img)
        cv.imshow('original_img', original_img)
        orig_img_h, orig_img_w, _ = original_img.shape

        # Cắt ảnh, loại bỏ phần biên 2 bên không cần thiết để dễ xử lý
        border = int(orig_img_w * CUT_BORDER)
        # cut_img = original_img[:, border:orig_img_w - border ]
        cut_img = original_img[:, 120:360]
        # cut_img = original_img
        cut_img_h, cut_img_w, _ = cut_img.shape

        cv.imshow('cut_img', cut_img)

        # Chuyển ảnh sang kênh màu xám
        draw_cut_img = cut_img.copy()
        gray_img = cv.cvtColor(cut_img, cv.COLOR_BGR2GRAY)
        
        #Làm min, giảm nhiễu
        blur_img = cv.GaussianBlur(gray_img, (7, 7), 1)
        # cv.imshow('blur_img', blur_img)
    
        # Lọc biên ảnh
        edges_img = cv.Canny(blur_img, 30, 60)
        # cv.imshow('edges_img', edges_img)

        kernel1 =  np.array([[-1, -1, -1],
                            [2, 2, 2],
                            [-1, -1, -1]])

        kernel2 =  np.array([[-1, -2, -1],
                            [0, 0, 0],
                            [1, 2, 1]])

        # edges_img1 = cv.filter2D(edges_img, -1, kernel1)
        # cv.imshow('x_filted_edges_img', edges_img1)

        edges_img2 = cv.filter2D(edges_img, -1, kernel1.T)
        # cv.imshow('y_filted_edges_img', edges_img2)
        
        sens_bottle = cv.getTrackbarPos('sensitivity', 'output')
        
        bottle_edge_list = fildHoughLines(edges_img2, sens_bottle, 1, 60, 100)

        if len(bottle_edge_list) == 0:
            continue
        
        min_x = min([row[0] for row in bottle_edge_list])
        max_x = max([row[0] for row in bottle_edge_list])
        if min_x == max_x:
            continue
        # cv.line(cut_img, (min_x, 0), (min_x, cut_img_h), (255, 255, 255), 2, cv.LINE_AA) 
        # cv.line(cut_img, (max_x, 0), (max_x, cut_img_h), (255, 255, 255), 2, cv.LINE_AA) 
        bottle_region = blur_img[0:cut_img_h, min_x:max_x]
        cv.imshow('bottle region', bottle_region)

        # edges_bottle = edges_img1[0:cut_img_h, min_x:max_x]
        min_thresh = cv.getTrackbarPos('min', 'output')
        max_thresh = cv.getTrackbarPos('max', 'output')

        edges_bottle_1 = cv.Canny(bottle_region, min_thresh, max_thresh)
        edges_bottle_1 = cv.filter2D(edges_bottle_1, -1, kernel1)
        # cv.imshow('x_filted_edges_img_1', edges_bottle_1)

        # pt0_list = fildHoughLines(edges_bottle, sens, 0)
        sens = cv.getTrackbarPos('sensitivity', 'output')
        pt0_list = fildHoughLines(edges_bottle_1, sens, 0, 20, 40)

        if len(pt0_list) == 0:
            continue

        pt0_array = np.asarray(pt0_list)
        pt0_y_array = np.sort(pt0_array[:, 1])[::-1]
        # print(pt0_y_array)

        # if len(pt0_y_array) == 0:
        #     continue

        # Xác định miệng, mức nước và đáy chai 
        point_idx_list = []
        level_list = [pt0_y_array[0]]

        tmp = pt0_y_array[0]
        for idx in range(1, len(pt0_y_array)):
            if (tmp - pt0_y_array[idx]) > 40:
                point_idx_list.append(idx)
                # print(pt0_y_array[idx])
                tmp = pt0_y_array[idx]
                level_list.append(tmp)

        # Xác định đáy
        # level_list[0] = pt0_y_array[point_idx_list[0]-1]
        # print(point_idx_list[0]-1)

        '''
        Vẽ đường thẳng ngang minh họa:
            màu vàng thể hiện vạch nắp chai,
            màu đỏ thể hiện vạch miệng chai,
            màu xanh lục thẻ hiện mực nước
            màu xanh lam thẻ hiện đáy chai
        '''
        for idx, val in enumerate(level_list):
            if idx > 2:
                break
            cv.line(draw_cut_img, (0, level_list[idx]), (cut_img_w, level_list[idx]), COLOR_VAL[idx], 2, cv.LINE_AA) 

        
        if len(level_list) > 2:

            # Xác định mức nước và miệng
            level_ratio = float(abs(level_list[2] - level_list[1])) / abs(level_list[1] - level_list[0])
            print(level_ratio, 3/7)
            if  0.38 <= level_ratio <= 0.45:
                cv.putText(draw_cut_img, 'Pass', (10, 20), cv.FONT_HERSHEY_SIMPLEX , 0.75, (255, 255, 255), 2)
            else:
                cv.putText(draw_cut_img, 'Fail', (10, 20), cv.FONT_HERSHEY_SIMPLEX , 0.75, (255, 255, 0), 2)

            #Xác định có nắp hay ko
            bottle_cap_region = bottle_region[0:level_list[2],:]
            cv.imshow("cap region", bottle_cap_region)
            thresh_value = cv.getTrackbarPos('cap thresh', 'output')
            ret, binary = cv.threshold(bottle_cap_region, thresh_value, 255, cv.THRESH_BINARY)
            cv.imshow("binary cap region", binary)
            nonzero = cv.countNonZero(binary)
            cap_pixel_ratio = 1 - float(nonzero) / (binary.shape[0] * binary.shape[1])
            print(cap_pixel_ratio)
            if cap_pixel_ratio > 0.2:
                cv.putText(draw_cut_img, 'Have cap', (60, 20), cv.FONT_HERSHEY_SIMPLEX , 0.6, (255, 120, 255), 2)

            
            # # level_list = []
            # # for i in pt0_y_array:
            # #     ratio = ((i - min_y) / (max_y - min_y))
            # #     if ratio > 0.15 and ratio < 0.85:
            # #         level_list.append(i)

        end = time.time()
        cv.putText(draw_cut_img, str(int(1 / (end-start))) + ' fps', (10, 45), cv.FONT_HERSHEY_SIMPLEX , 0.6, (127, 255, 127), 1)

        cv.imshow("output_draw", draw_cut_img)
     
        if cv.waitKey(30) & 0xff == ord('q'):
            break
    
    cv.destroyAllWindows()