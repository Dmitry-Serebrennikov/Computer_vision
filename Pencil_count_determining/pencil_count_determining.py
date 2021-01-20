import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import morphology
from skimage.measure import label, regionprops
from skimage.filters import try_all_threshold, threshold_triangle

def toGray(image):
    return (0.2989 * image[:, :, 0] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 2]).astype("uint8")

def binarization(image, limit_min, limit_max):
    B = image.copy()
    B[B <= limit_min] = 0
    B[B >= limit_max] = 0
    B[B > 0] = 1
    return B

def hist(gray):
    H = np.zeros(256)
    for i in range(gray.shape[0]):
        for j in range(gray.shape[1]):
            val = gray[i, j]
            H[val] += 1
    return H

def circularity(region, label = 1):
    return (region.perimeter ** 2) / region.area

img = 0
pencil_count = 0

for img in range(1, 13):
    image = plt.imread("images/img ("+str(img)+").jpg")
    gray = toGray(image)
    thresh = threshold_triangle(gray)
    binary = binarization(gray, 0, thresh)
    binary = morphology.binary_dilation(binary, iterations = 1)

#try_all_threshold(gray, figsize=(12, 10), verbose=False)
#H = hist(gray)
#binary = binarization(gray, 118, 179)

    labeled = label(binary)
    areas = []
    
    for region in regionprops(labeled):
        areas.append(region.area)

#print(np.mean(areas))
#print(np.median(areas))

    for region in regionprops(labeled):
        if region.area < np.mean(areas):
            labeled[labeled == region.label] = 0
        bbox = region.bbox
        if bbox[0] == 0 or bbox[1] == 0:
            labeled[labeled == region.label] = 0
            
    labeled[labeled > 0] = 1
    labeled = label(labeled)
    
    cnt = 0
    lbl = 0
    for reg in regionprops(labeled):
        lbl += 1
        if (((circularity(reg, lbl) > 100) and (300000 < reg.area < 500000))):
            cnt += 1
    
    print("img ("+str(img)+").jpg : number of pencils = ", cnt)
    pencil_count += cnt
    
print("Total number of pencils: ", pencil_count)

#plt.subplot(131)
#plt.imshow(gray, cmap="gray") #
#plt.subplot(132)
#plt.imshow(binary)
#plt.subplot(133)
#plt.imshow(labeled)

#plt.show()