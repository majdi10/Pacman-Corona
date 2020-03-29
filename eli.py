import cv2
import numpy
import random
from matplotlib import pyplot as plt
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

painted_pixels = 0
bfs_arr = []
center = []
min_height = 0
max_height = 0
min_width = 0
max_width = 0


def check_min_max_height_width(x, y):
    global min_height, max_height, min_width, max_width
    if x < min_height:
        min_height = x
    if x > max_height:
        max_height = x
    if y < min_width:
        min_width = y
    if y > max_width:
        max_width = y


def bfs(x, y, color):
    global painted_pixels, bfs_arr

    if x + 1 < image.shape[0]:
        if sum(image[x + 1][y]) == 0:  # if black
            bfs_arr.insert(0, [x + 1, y, color])
            image[x + 1][y] = color
            painted_pixels -= 1
            check_min_max_height_width(x+1, y)

    if y + 1 < image.shape[1]:
        if sum(image[x][y + 1]) == 0:  # if black
            bfs_arr.insert(0, [x, y + 1, color])
            image[x][y + 1] = color
            painted_pixels -= 1
            check_min_max_height_width(x, y + 1)

    if x + 1 < image.shape[0] and y + 1 < image.shape[1]:
        if sum(image[x + 1][y + 1]) == 0:  # if black
            bfs_arr.insert(0, [x + 1, y + 1, color])
            image[x + 1][y + 1] = color
            painted_pixels -= 1
            check_min_max_height_width(x + 1, y + 1)

    if x + 1 < image.shape[0] and y - 1 >= 0:
        if sum(image[x + 1][y - 1]) == 0:  # if black
            bfs_arr.insert(0, [x + 1, y - 1, color])
            image[x + 1][y - 1] = color
            painted_pixels -= 1
            check_min_max_height_width(x + 1, y - 1)

    if y - 1 >= 0:
        if sum(image[x][y - 1]) == 0:  # if black
            bfs_arr.insert(0, [x, y - 1, color])
            image[x][y - 1] = color
            painted_pixels -= 1
            check_min_max_height_width(x, y - 1)

    if x - 1 >= 0:
        if sum(image[x - 1][y]) == 0:  # if black
            bfs_arr.insert(0, [x - 1, y, color])
            image[x - 1][y] = color
            painted_pixels -= 1
            check_min_max_height_width(x - 1, y)

    if x - 1 >= 0 and y - 1 >= 0:
        if sum(image[x - 1][y - 1]) == 0:  # if black
            bfs_arr.insert(0, [x - 1, y - 1, color])
            image[x - 1][y - 1] = color
            painted_pixels -= 1
            check_min_max_height_width(x - 1, y - 1)

    if x - 1 >= 0 and y + 1 < image.shape[1]:
        if sum(image[x - 1][y + 1]) == 0:  # if black
            bfs_arr.insert(0, [x - 1, y + 1, color])
            image[x - 1][y + 1] = color
            painted_pixels -= 1
            check_min_max_height_width(x - 1, y + 1)

    # check_min_max_height_width(x, y)
    # image[x][y] = color
    # painted_pixels -= 1

    bfs_arr.pop()


def s(passed_image):
    global painted_pixels, bfs_arr, min_height, max_height, min_width, max_width

    for row in range(len(passed_image)):
        for col in range(len(passed_image[row])):

            if sum(passed_image[row][col]) == 0:  # if black pixel
                # started = True
                rgb = [random.randrange(255), random.randrange(255), random.randrange(254)]
                white = [255, 255, 255]
                painted_pixels = 150
                passed_image[row][col] = white
                bfs_arr = [[row, col, white]]

                min_height = passed_image.shape[0]
                max_height = 0

                min_width = passed_image.shape[1]
                max_width = 0

                # while len(bfs_arr) > 0:
                #     while painted_pixels > 0 and len(bfs_arr) > 0:
                #         bfs(bfs_arr[len(bfs_arr)-1][0], bfs_arr[len(bfs_arr)-1][1], [255, 255, 255])
                #         # print(row, col, painted_pixels, len(bfs_arr))
                #
                #     center.append([min_height, max_height, min_width, max_width])
                #     painted_pixels = 700
                #
                #     min_height = image.shape[0]
                #     max_height = 0
                #
                #     min_width = image.shape[1]
                #     max_width = 0
                #
                # return

                while len(bfs_arr) > 0 and painted_pixels > 0:
                    bfs(bfs_arr[len(bfs_arr)-1][0], bfs_arr[len(bfs_arr)-1][1], rgb)

                # if painted_pixels < painted_pixels_copy * 0.1:
                if painted_pixels == 0:
                    center.append([min_height, max_height, min_width, max_width])


if __name__ == '__main__':
    image = cv2.imread('map.PNG')
    image_copy = image.copy()
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    print(image.shape)
    s(image)
    print("Done painting image")
    print(len(center))
    coins_num = 0
    for i in center:
        row_y = int((i[0] + i[1]) / 2)
        col_x = int((i[2] + i[3]) / 2)
        # if sum(image_copy[row_y][col_x]) == 0:
        #     image_copy[row_y][col_x] = [54, 136, 181]

        added = []
        coin_outside = False
        r = 5
        for ball_y in range(-r, r):
            for ball_x in range(-r, r):
                if pow(ball_y, 2) + pow(ball_x, 2) <= r \
                        and image_copy.shape[0] - 1 > row_y + ball_y >= 0 \
                        and image_copy.shape[1] - 1 > col_x + ball_x >= 0:
                    if sum(image_copy[row_y + ball_y][col_x + ball_x]) == 0:
                        added.append([row_y+ball_y, col_x+ball_x])
                    else:
                        coin_outside = True
        # Detect and delete coins that got sliced. only perfect coins!
        if coin_outside is False:
            coins_num += 1
            for pixel in added:
                image_copy[pixel[0]][pixel[1]] = [255, 0, 0]

    print(coins_num)
    # cv2.imwrite("food.png", image_copy)
    plt.figure(figsize=[50, 20])
    plt.subplot(131)
    plt.imshow(image_copy, cmap='gray')
    plt.show()
