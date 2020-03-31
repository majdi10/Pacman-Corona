from tkinter import *
import cv2
# pip install pillow
from PIL import Image, ImageTk
import eli
import numpy as np
import time
import threading
import enum


class HorizontalDirection(enum.Enum):
    LEFT = 1
    RIGHT = 2


class VerticalDirection(enum.Enum):
    UP = 1
    DOWN = 2


horizontal_direction = HorizontalDirection.RIGHT
vertical_direction = VerticalDirection.UP
pacman_y = 0
pacman_x = 0
moves = []
first_time_click = True
last_move = None


def a(event):
    global horizontal_direction, vertical_direction, first_time_click
    if event.char == "w":
        vertical_direction = VerticalDirection.UP
        if first_time_click:
            move()
            first_time_click = False
    if event.char == "s":
        vertical_direction = VerticalDirection.DOWN
        if first_time_click:
            move()
            first_time_click = False
    if event.char == "a":
        horizontal_direction = HorizontalDirection.LEFT
        if first_time_click:
            move()
            first_time_click = False
    if event.char == "d":
        horizontal_direction = HorizontalDirection.RIGHT
        if first_time_click:
            move()
            first_time_click = False


def pacman_next_move(center_y, center_x, og_map):
    center_y += int(pacman_width / 2)
    center_x += int(pacman_height / 2)
    next_moves = []

    if np.array_equal(og_map[center_x-1][center_y-1], np.asarray(eli.LINE_COLOR)):
        next_moves.append([-1, -1])
    if np.array_equal(og_map[center_x-1][center_y], np.asarray(eli.LINE_COLOR)):
        next_moves.append([-1, 0])
    if np.array_equal(og_map[center_x-1][center_y+1], np.asarray(eli.LINE_COLOR)):
        next_moves.append([-1, 1])
    if np.array_equal(og_map[center_x][center_y-1], np.asarray(eli.LINE_COLOR)):
        next_moves.append([0, -1])
    if np.array_equal(og_map[center_x][center_y+1], np.asarray(eli.LINE_COLOR)):
        next_moves.append([0, 1])
    if np.array_equal(og_map[center_x+1][center_y - 1], np.asarray(eli.LINE_COLOR)):
        next_moves.append([1, -1])
    if np.array_equal(og_map[center_x+1][center_y], np.asarray(eli.LINE_COLOR)):
        next_moves.append([1, 0])
    if np.array_equal(og_map[center_x+1][center_y+1], np.asarray(eli.LINE_COLOR)):
        next_moves.append([1, 1])
    if vertical_direction == VerticalDirection.UP and horizontal_direction == HorizontalDirection.RIGHT:
        next_moves = sorted(next_moves, key=lambda x: [x[0], -x[1]])
    elif vertical_direction == VerticalDirection.UP and horizontal_direction == HorizontalDirection.LEFT:
        next_moves = sorted(next_moves, key=lambda x: [x[0], x[1]])
    elif vertical_direction == VerticalDirection.DOWN and horizontal_direction == HorizontalDirection.RIGHT:
        next_moves = sorted(next_moves, key=lambda x: [-x[0], -x[1]])
    else:
        next_moves = sorted(next_moves, key=lambda x: [-x[0], x[1]])

    # Attempt to stop pacman from running back and forward in end of road
    if next_moves[0] == last_move:
        next_moves.pop()
        if len(next_moves) == 0:
            return None
    return next_moves[0]


def move():
    global pacman_y, pacman_x, last_move
    last_move = [pacman_x, pacman_y]
    next_move = pacman_next_move(pacman_x, pacman_y, cv2_map_img)
    if next_move is not None:
        pacman_y = pacman_y + next_move[0]
        pacman_x = pacman_x + next_move[1]
        canvas.move(pacman_image, next_move[1], next_move[0])
    # else:

    # return
    canvas.after(10, move)


if __name__ == '__main__':
    # Create the window with the Tk class
    root = Tk()

    # Create the canvas and make it visible with pack()
    canvas = Canvas(root, width=1197, height=734)
    canvas.grid(row=2, column=3)
    canvas.pack()  # this makes it visible

    # Loads and create image (put the image in the folder)
    map_img = PhotoImage(file="food.png")
    map_image = canvas.create_image(0, 0, anchor=NW, image=map_img)

    img = Image.open("demo.png")

    pacman_width = 10
    pacman_height = 10
    cv2_map_img = cv2.imread('food.png')
    found = False
    for row in range(200, cv2_map_img.shape[0]):
        if found is False:
            for col in range(100, cv2_map_img.shape[1]):
                if np.array_equal(cv2_map_img[row][col], np.asarray(eli.LINE_COLOR)) and found is False:
                    # pacman_x = row - pacman_img.shape[0]/2
                    # pacman_y = col + pacman_img.shape[1]/2
                    pacman_x = col - int(pacman_width/2)
                    pacman_y = row - int(pacman_height/2)
                    print(row, col)
                    found = True
                    break
        else:
            break

    # image = Image.open("demo.png")
    # image = image.resize((50, 50))

    img = img.resize((pacman_width, pacman_height), Image.ANTIALIAS)
    photoImg = ImageTk.PhotoImage(img)
    # pacman_x = 100
    # pacman_y = 100
    pacman_image = canvas.create_image(pacman_x, pacman_y, anchor=NW, image=photoImg)

    # This bind window to keys so that move is called when you press a key
    root.bind("<Key>", a)

    # t1 = threading.Thread(target=move())
    # t1.start()
    # print("asd")

    root.mainloop()

# root = Tk()
# app = Window(root)
# root.wm_title("Tkinter window")
# root.geometry("1197x734")
# root.mainloop()
# while True:
#     time.sleep(0.1)
#     app.move_pacman()
#     root.mainloop()


