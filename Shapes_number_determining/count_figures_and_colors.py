import matplotlib.pyplot as plt
from skimage.filters import sobel, threshold_isodata
from skimage.morphology import binary_closing, binary_opening
from skimage.measure import label, regionprops
import numpy as np
from skimage import color


def count_colors(figures):
    colors = {"red" : 0, "orange" : 0, "yellow" : 0, "green" : 0, "blue" : 0, "dark_blue" : 0, "purple" : 0}
    #Hue – оттенок от 0° до 360° (красный, оранжевый, желтый, зеленый, голубой, синий, фиолетовый)
    # red 0 - 15 and 330 - 360 orange: 15 - 45 yellow = 45 - 90 green: 90 - 150 blue: 150-210 dark blue: 210-270 purple: 270-330
    for hue in figures:
            
        if (0 <= hue < 15 or 330 <= hue <= 360):
            colors['red'] += 1
        elif (15 <= hue < 45):
            colors['orange'] += 1
        elif (45 <= hue < 90):
            colors['yellow'] += 1
        elif (90 <= hue < 150):
            colors['green'] += 1
        elif (150 <= hue < 210):
            colors['blue'] += 1
        elif (210 <= hue < 270):
            colors['dark_blue'] += 1
        elif (270 <= hue < 330):
            colors['purple'] += 1

    return colors


image = plt.imread("balls_and_rects.png")
binary = image.copy()[:, :, 0]
binary[binary > 0] = 1

image = color.rgb2hsv(image)[:, :, 0] * 360

labeled = label(binary)

balls = []
rects = []

print("Total number of figures:", np.max(labeled))

for region in regionprops(labeled):
    y1, x1, y2, x2 = region.bbox
    val = np.max(image[y1:y2, x1:x2])
    if region.extent == 1:
        rects.append(val)
    else:
        balls.append(val)

print("Number of Rects:", len(rects))
rectangle_colors = count_colors(rects)
print(rectangle_colors)
        
print("Number of balls:", len(balls))
ball_colors = count_colors(balls)
print(ball_colors)


plt.figure()
plt.imshow(image)
plt.show()