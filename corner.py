import cv2
import numpy as np

cap = cv2.VideoCapture('demo.mp4')
cv2.waitKey(0)

while(cap.isOpened()):
    ret, img = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([20,100,100])
    upper_yellow = np.array([30,255,255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130,240,240])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    lower_red = np.array([0,95,95])
    upper_red = np.array([10,255,255])
    mask_red = cv2.inRange(hsv, lower_red, upper_red)

    mask_total = 255*(mask_yellow + mask_blue + mask_red)
    
    result = cv2.bitwise_and(img, img, mask=mask_total)
    if ret == True:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        image = np.zeros(img.shape, np.uint8)
        image = cv2.resize(img, (0,0), fx = 0.5, fy = 1)
        
        corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 0)
        corners = np.int0(corners)
        
        cornerdic = {}

        for corner in corners:
            x, y = corner.ravel()
            cornerdic[int((x*x + y*y)**0.5)] = [x, y]

        cornerdic2 = {}

        for keys in sorted(cornerdic.keys()):
            cornerdic2[keys] = cornerdic[keys]

        prev = -99
        thres = 100
        rect = []
        rects = []

        for key in cornerdic2.keys():
            if abs(key - prev) <= thres:
                rect.append(cornerdic2[key])
            else:
                xa = []
                ya = []
                for p in rect:
                    xa.append(p[0])
                    ya.append(p[1])
                rect = []
                if len(xa) > 0 and len(ya) > 0:
                   rects.append([(min(xa),min(ya)), (max(xa), max(ya))]) 
            prev = key
            
        for r in rects:
            cv2.rectangle(img, r[0], r[1], (255, 0, 0), 2)

        smol_mountain = cv2.resize(img, (0,0), fx = 0.5, fy = 0.5)
        smol_ore = cv2.resize(result, (0,0), fx = 0.5, fy = 0.5)
        
        image[:height//2, :width//2] = smol_mountain
        image[height//2:, :width//2] = smol_ore

        image = cv2.resize(image, (0, 0), fx = 0.7, fy = 0.7)
        
        cv2.imshow("rover camera", image)
        cv2.waitKey(1)  
    else:
        break

cap.release()
cv2.destroyAllWindows()
