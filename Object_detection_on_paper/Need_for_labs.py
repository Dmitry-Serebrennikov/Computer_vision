import cv2
import numpy as np
import matplotlib.pyplot as plt

flimit = 250
slimit = 255

def fupdate(value):
    global flimit
    flimit = value
    
def supdate(value):
    global slimit
    slimit = value

template_picture = cv2.imread("4labs.png")    

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_EXPOSURE, 3)

cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("Mask", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("Paper", cv2.WINDOW_KEEPRATIO)

cv2.createTrackbar("F", "Mask", flimit, 255, fupdate)
cv2.createTrackbar("S", "Mask", slimit, 255, supdate)

kernel = np.ones((7, 7))

while cam.isOpened():
    
    ret, frame = cam.read()
    
    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    mask = cv2.inRange(converted, np.array([10, flimit, 10]), np.array([100, slimit, 255]))
    mask = cv2.erode(mask, kernel)
    mask = cv2.dilate(mask, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    contours =  cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(contours) > 0:
        paper = max(contours, key = cv2.contourArea)
        rect = cv2.minAreaRect(paper)
        box = cv2.boxPoints(rect)
        box_x = []
        box_y = []
        for p in box:
            cv2.circle(frame, tuple(p), 6, (0, 0 , 255), 2)
            box_x.append(int(p[0]))
            box_y.append(int(p[1]))
            if box_x:
                paper_frame = frame[min(box_y): max(box_y), min(box_x):max(box_x)]
                if paper_frame.size > 0 and len(box_x) == 4 and (len(box_y) == 4):
                    paper_edges = np.float32([(box_x[0], box_y[0]), (box_x[3], box_y[3]),
                                               (box_x[1], box_y[1]), (box_x[2], box_y[2])])
                    paper_standart_A4 = np.float32([[0, 0], [0, 210], [297, 0], [297, 210]])
                    perspective = cv2.getPerspectiveTransform(paper_edges, paper_standart_A4)
                    perspective_paper_frame = cv2.warpPerspective(frame, perspective, (297, 210))
                    cv2.imshow("Paper", perspective_paper_frame)
                    
                    forlabs_match = cv2.matchTemplate(perspective_paper_frame, template_picture, cv2.TM_CCOEFF_NORMED)
                    _, value, _, _  = cv2.minMaxLoc(forlabs_match)
                    #print(value)
                    if value > 0.30:
                        cv2.putText(frame, "FORLABS IS HERE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0))
                
        cv2.drawContours(frame, [np.int0(box)], 0, (0, 255, 0), 2)
        #paper = max(contours, key = cv2.contourArea)
        #hull = cv2.convexHull(paper)
        #for i in range(1, len(hull)):
            #cv2.line(frame, tuple(*hull[i-1]), tuple(*hull[i]), (0, 255, 0), 2)
        #cv2.line(frame, tuple(*hull[i-1]), tuple(*hull[0]), (0, 255, 0), 2)
        
        cv2.drawContours(frame, [paper], -1, (0, 255, 0), 3)
    
    cv2.imshow("Camera", frame)
    cv2.imshow("Mask", mask)
    
    key = cv2.waitKey(1)
    if key == ord('p'):
        cv2.imwrite("screenshot_new_paper.png", np.hstack([frame[:,:,0], mask, aff_img]))
    if key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()