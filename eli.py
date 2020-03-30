import collections

import cv2
import numpy as np
import random
from matplotlib import pyplot as plt
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from scipy.spatial import distance

CHOSE_PAINTED_PIXELS = 80
painted_pixels = 0
bfs_arr = []
center = []
centers = []
min_height = 0
max_height = 0
min_width = 0
max_width = 0
LINE_COLOR = [100, 40, 255]
COIN_RADIUS = 4


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


def bfs(passed_image, x, y, color):
    global painted_pixels, bfs_arr
    if x + 1 < passed_image.shape[0]:
        if sum(passed_image[x + 1][y]) == 0:  # if black
            bfs_arr.insert(0, [x + 1, y, color])
            passed_image[x + 1][y] = color
            painted_pixels -= 1
            check_min_max_height_width(x+1, y)

    if y + 1 < passed_image.shape[1]:
        if sum(passed_image[x][y + 1]) == 0:  # if black
            bfs_arr.insert(0, [x, y + 1, color])
            passed_image[x][y + 1] = color
            painted_pixels -= 1
            check_min_max_height_width(x, y + 1)

    if x + 1 < passed_image.shape[0] and y + 1 < passed_image.shape[1]:
        if sum(passed_image[x + 1][y + 1]) == 0:  # if black
            bfs_arr.insert(0, [x + 1, y + 1, color])
            passed_image[x + 1][y + 1] = color
            painted_pixels -= 1
            check_min_max_height_width(x + 1, y + 1)

    if x + 1 < passed_image.shape[0] and y - 1 >= 0:
        if sum(passed_image[x + 1][y - 1]) == 0:  # if black
            bfs_arr.insert(0, [x + 1, y - 1, color])
            passed_image[x + 1][y - 1] = color
            painted_pixels -= 1
            check_min_max_height_width(x + 1, y - 1)

    if y - 1 >= 0:
        if sum(passed_image[x][y - 1]) == 0:  # if black
            bfs_arr.insert(0, [x, y - 1, color])
            passed_image[x][y - 1] = color
            painted_pixels -= 1
            check_min_max_height_width(x, y - 1)

    if x - 1 >= 0:
        if sum(passed_image[x - 1][y]) == 0:  # if black
            bfs_arr.insert(0, [x - 1, y, color])
            passed_image[x - 1][y] = color
            painted_pixels -= 1
            check_min_max_height_width(x - 1, y)

    if x - 1 >= 0 and y - 1 >= 0:
        if sum(passed_image[x - 1][y - 1]) == 0:  # if black
            bfs_arr.insert(0, [x - 1, y - 1, color])
            passed_image[x - 1][y - 1] = color
            painted_pixels -= 1
            check_min_max_height_width(x - 1, y - 1)

    if x - 1 >= 0 and y + 1 < passed_image.shape[1]:
        if sum(passed_image[x - 1][y + 1]) == 0:  # if black
            bfs_arr.insert(0, [x - 1, y + 1, color])
            passed_image[x - 1][y + 1] = color
            painted_pixels -= 1
            check_min_max_height_width(x - 1, y + 1)

    # check_min_max_height_width(x, y)
    # image[x][y] = color
    # painted_pixels -= 1

    bfs_arr.pop()


def draw_coins(passed_image):
    global painted_pixels, bfs_arr, min_height, max_height, min_width, max_width, CHOSE_PAINTED_PIXELS, centers, center, COIN_RADIUS
    image_copy = passed_image.copy()

    # Step 1
    for row in range(len(passed_image)):
        for col in range(len(passed_image[row])):

            if sum(passed_image[row][col]) == 0:  # if black pixel
                # started = True
                rgb = [random.randrange(255), random.randrange(255), random.randrange(254)]
                white = [255, 255, 255]
                painted_pixels = CHOSE_PAINTED_PIXELS
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
                    bfs(passed_image, bfs_arr[len(bfs_arr)-1][0], bfs_arr[len(bfs_arr)-1][1], rgb)

                # if painted_pixels < painted_pixels_copy * 0.1:
                if painted_pixels == 0:
                    center.append([min_height, max_height, min_width, max_width])

    # Step 2
    #  Might put this in new function
    # coins_num = 0
    for i in center:
        row_y = int((i[0] + i[1]) / 2)
        col_x = int((i[2] + i[3]) / 2)
        # if sum(image_copy[row_y][col_x]) == 0:
        #     image_copy[row_y][col_x] = [54, 136, 181]

        added = []
        coin_outside = False
        for ball_y in range(-COIN_RADIUS, COIN_RADIUS):
            for ball_x in range(-COIN_RADIUS, COIN_RADIUS):
                if pow(ball_y, 2) + pow(ball_x, 2) <= COIN_RADIUS \
                        and image_copy.shape[0] - 1 > row_y + ball_y >= 0 \
                        and image_copy.shape[1] - 1 > col_x + ball_x >= 0:
                    if sum(image_copy[row_y + ball_y][col_x + ball_x]) == 0:
                        added.append([row_y + ball_y, col_x + ball_x])
                    else:
                        coin_outside = True

        # Detect and delete coins that got sliced. only perfect coins!
        if coin_outside is False:
            for pixel in added:
                image_copy[pixel[0]][pixel[1]] = [255, 0, 0]
                if row_y == pixel[0] and col_x == pixel[1]:
                    centers.append([row_y, col_x])

    # print(coins_num)
    return image_copy


def draw_lines(passed_image):
    global centers, LINE_COLOR
    sorted_centers = sort_centers()
    for i in range(len(sorted_centers) - 1):
        image_copy = og_image.copy()
        cv2.line(image_copy, (sorted_centers[i][1], sorted_centers[i][0]),
                 (sorted_centers[i + 1][1], sorted_centers[i + 1][0]), tuple(LINE_COLOR), 1)

        xs = [sorted_centers[i][1], sorted_centers[i+1][1]]
        ys = [sorted_centers[i][0], sorted_centers[i+1][0]]
        color_ok = True
        for y in range(min(ys), max(ys)+1):
            if color_ok:
                for x in range(min(xs), max(xs)+1):
                    # print(og_image[y][x], np.asarray(LINE_COLOR))
                    if np.array_equal(image_copy[y][x], np.asarray(LINE_COLOR)):
                        if sum(og_image[y][x]) != 0:
                            color_ok = False

        if color_ok:
            cv2.line(passed_image, (sorted_centers[i][1], sorted_centers[i][0]),
                     (sorted_centers[i + 1][1], sorted_centers[i + 1][0]), tuple(LINE_COLOR), 1)
    return passed_image


def sort_centers():
    global centers
    sorted_arr = [centers[0]]
    chosen = sorted_arr[0]
    centers.pop()
    first_iter = True
    while len(centers) > 0:
        min_distance = sys.maxsize
        remember_index = 0
        for i in range(len(centers)):
            euc_distance = distance.euclidean([chosen[1], chosen[0]], [centers[i][1], centers[i][0]])
            if euc_distance < min_distance:
                min_distance = euc_distance
                remember_index = i
        sorted_arr.append(centers[remember_index])
        chosen = centers[remember_index]
        if first_iter:
            first_iter = False
        else:
            centers = centers[:remember_index] + centers[remember_index + 1:]

    return sorted_arr


if __name__ == '__main__':
    og_image = cv2.imread('map.PNG')

    # image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    print(og_image.shape)
    coins_image = draw_coins(og_image.copy())
    print("Done painting image")
    print("Number of perfect coins: " + str(len(center)))
    lines_coins_image = draw_lines(coins_image.copy())

    cv2.imwrite("food.png", lines_coins_image)
    # plt.figure(figsize=[15, 7])
    # plt.subplot(131)
    # plt.imshow(lines_coins_image)
    # plt.imshow(og_image, cmap='gray')
    # plt.show()


