import time
import matplotlib.pyplot as plt
import pyautogui
from mss import mss
import cv2
import numpy as np


def screen():
    with mss() as sct:
        filename = sct.shot()
        image = cv2.imread(filename)
        return image
    
def findField(original):
    image = original[100:-100, 100:-100]
    
    for i in range(image.shape[0] - 1):
        for j in range(image.shape[1] - 1):
            line_pixels = 0
            if image[i, j, 0] < 180 and image[i, j, 0] > 90:
                for w in range(30):
                    for h in range(1):
                        if image[i+h, j+w, 0]>180 or image[i+h, j+w, 0]<90:
                            break
                        else:
                            line_pixels += 1 
                if line_pixels == 30:
                    return j, i
    return 0, 0
            

if __name__ == "__main__":

    time.sleep(3)
    pyautogui.press('up')
    time.sleep(1)
    image = screen()
    x_start, y_start = findField(image)
    x_start = x_start+100
    y_start = y_start+100
    x_finish, y_finish = findField(image[:, ::-1])
    x_finish = image.shape[1] - x_finish - 100
    y_finish = y_finish+100
    background_color = image[100, 100]
    
    obstacle_line = y_start - int((x_finish - x_start)*0.04)
    print(x_start, y_start, x_finish, y_finish, obstacle_line)

    #image[y_start: y_finish+1, x_start:x_finish] = (0, 255, 0)
    #plt.imshow(image)
    #plt.show()  

    time.sleep(3)
    while True:
        image = screen()
        for i in range(int((x_start+x_finish)/2-150), int((x_start+x_finish)/2)-100):
            diff = np.zeros(3)
            for k in range (3):
                diff[k] = image[obstacle_line, i, k] - background_color[k]     

            if any(c > 20 for c in diff):
                pyautogui.press('up')
                break