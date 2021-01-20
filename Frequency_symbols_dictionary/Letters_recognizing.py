import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import morphology
from skimage.measure import label, regionprops
from skimage.filters import try_all_threshold, threshold_triangle, threshold_otsu

def lakes(image):
    B = ~image
    BB = np.ones((B.shape[0] + 2, B.shape[1] + 2))
    BB[1:-1, 1:-1] = B
    return np.max(label(BB)) - 1

def has_vline(image):
    lines = np.sum(image, 0) // image.shape[0]
    return 1 in lines

def has_hline(image):
    lines = np.sum(image, 1) // image.shape[1]
    return 1 in lines

def has_bay(image):
    b = ~image
    bb = np.zeros((b.shape[0] + 1, b.shape[1])).astype("uint8")
    bb[:-1, :] = b
    return lakes(~bb) - 1

def count_bays(image):
    holes = ~image.copy()
    return np.max(label(holes))

def recognize(region):
    lc = lakes(region.image)
    bays = count_bays(region.image)
    circularity = region.perimeter ** 2 / region.area    
    
    if lc == 0:
        #print("1 or w or x or * or - or /")
        if bays == 0:
            return "-"
        elif bays == 3 and has_vline(region.image):
            return "1"
        elif bays == 2:
            return "/"
        
        elif bays == 5:
            #print("W or *")
            if has_hline(region.image) and circularity < 50:
                return "*"
            else:
                return "W"
        else:
            #print("X or *")
            if bays == 4 and circularity > 40:
                return "X"
            else:
                return "*"
    
    elif lc == 1:
        #print("A or 0 or P or D")
        if has_bay(region.image) > 0:
            return "A"
        elif has_vline(region.image) and bays == 3:
            if circularity > 58:
                return "D"
            else:
                return "P"
        elif bays >= 4:
            return "0"
    
    elif lc == 2:
        #print("8 or B")
        if has_vline(region.image) and bays <= 4:
            return "B"
        else:
            return "8"
            
    return None

image = plt.imread("symbols.png")
#print(image.shape)
image = np.sum(image, 2)
#print(image.shape)
image[image > 0] = 1

labeled = label(image)
#print(np.max(labeled))

regions = regionprops(labeled)

d = {}

for region in regions:
    symbol = recognize(region)
    if symbol not in d:
        d[symbol] = 1
    else:
        d[symbol] += 1

        
print("Total number of symbols: ", sum(d.values()))
print(d)

for key in d.keys():
    percent = d.get(key) / sum(d.values()) * 100
    print(key," - ", percent, "%")

#plt.figure()
#plt.subplot(121)
#plt.imshow(image)
#plt.subplot(122)
#plt.imshow(labeled)
#plt.show()