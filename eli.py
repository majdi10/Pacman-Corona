import cv2
import numpy
import random
from matplotlib import pyplot as plt
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

painted_pixels = 0
bfs_arr = []


def bfs(x, y, color):
    global painted_pixels, bfs_arr
    if x + 1 < image.shape[0]-1 and painted_pixels > 0:
        if sum(image[x + 1][y]) == 0:  # if black
            bfs_arr.insert(0, [x + 1, y, color])
            image[x + 1][y] = color
            painted_pixels -= 1
    if y + 1 < image.shape[1]-1 and painted_pixels > 0:
        if sum(image[x][y + 1]) == 0:  # if black
            bfs_arr.insert(0, [x, y + 1, color])
            image[x][y + 1] = color
            painted_pixels -= 1
    if x + 1 < image.shape[0]-1 and y + 1 < image.shape[1]-1 and painted_pixels > 0:
        if sum(image[x + 1][y + 1]) == 0:  # if black
            bfs_arr.insert(0, [x + 1, y + 1, color])
            image[x + 1][y + 1] = color
            painted_pixels -= 1
    bfs_arr.pop()


if __name__ == '__main__':
    image = cv2.imread('map.PNG')
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    started = False
    pixel_width = 50
    pixel_height = 50
    MAX_PAINTED_PIXELS = 50
    before_black = False
    print(image.shape)
    for row in range(len(image) - pixel_width):
        for col in range(len(image[row]) - pixel_height):

            if sum(image[row][col]) == 0:  # if black pixel
                # started = True
                r = random.randrange(255)
                g = random.randrange(255)
                b = random.randrange(254)
                painted_pixels = 300
                image[row][col] = [r, g, b]
                bfs_arr = [[row, col, [r, g, b]]]
                while len(bfs_arr) > 0 and painted_pixels > 0:
                    bfs(bfs_arr[0][0], bfs_arr[0][1], [r, g, b])
                # for i in range(row, row+pixel_width):
                #     for j in range(col, col+pixel_height):
                #         if sum(image[i][j]) != 765:
                #             # image[i][j] = random.randrange(20, 220)
                #             before_black = TRUE
                #             image[i][j] = [r, g, b]
                #             painted_pixels -= 1
                #             if painted_pixels < 0:
                #                 painted_pixels = 0

    plt.figure(figsize=[50,20])
    plt.subplot(131)
    plt.imshow(image, cmap='gray')
    # image[:100,:100] = 0
    plt.show()
