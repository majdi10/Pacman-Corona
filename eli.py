import cv2
import numpy
import random
from matplotlib import pyplot as plt
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog


image = cv2.imread('map.PNG')
# image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)




started = False
pixel_width = 50
pixel_height = 50
painted_pixels = 0
MAX_PAINTED_PIXELS = 50

print(image.shape)
for row in range(len(image)):
    for col in range(len(image[row])):
        if sum(image[row][col]) == 0 and started is False:
            # started = True
            r = random.randrange(255)
            g = random.randrange(255)
            b = random.randrange(255)
            for i in range(pixel_width):
                for j in range(pixel_height):
                    if sum(image[i][j]) != 765:
                        image[i][j] = [r, g, b]

plt.figure(figsize=[50,20])
plt.subplot(131)
plt.imshow(image, cmap='gray')
# image[:100,:100] = 0
plt.show()
