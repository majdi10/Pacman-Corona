from tkinter import *
import cv2
# pip install pillow
from PIL import Image, ImageTk
import eli
import numpy as np
import time

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)

        load = Image.open("food.PNG")
        self.render = ImageTk.PhotoImage(load)
        img = Label(self, image=self.render)
        img.image = self.render
        img.place(x=0, y=0)

        pacman_x = 0
        pacman_y = 0

        pacman_resize_height = 50
        pacman_resize_width = 50

        # pacman_img = cv2.imread('pacman.png')
        map_img = cv2.imread('food.png')
        for row in range(map_img.shape[0]):
            for col in range(map_img.shape[1]):
                if np.array_equal(map_img[row][col], np.asarray(eli.LINE_COLOR)):
                    # pacman_x = row - pacman_img.shape[0]/2
                    # pacman_y = col + pacman_img.shape[1]/2
                    pacman_x = row - pacman_resize_height / 2
                    pacman_y = col + pacman_resize_width / 2
                    break

        self.pacman = tk.create_image(480, 258, image=self.image, anchor=tk.NW)
        # pacman_img = Image.open("pacman.png")
        # pacman_img = pacman_img.resize((pacman_resize_height, pacman_resize_width), Image.ANTIALIAS)
        # self.render = ImageTk.PhotoImage(pacman_img)
        # self.pacman = Label(self, image=self.render)
        # self.pacman.image = self.render
        # self.pacman.place(x=pacman_x, y=pacman_y)
        # self.center_x = int(pacman_x)
        # self.center_y = int(pacman_y)
        # self.move = "right"
        # self.map = map_img

    def move_pacman(self):
        next_move = []
        print(self.center_y, self.center_x)
        if np.array_equal(self.map[self.center_x-1][self.center_y-1], np.asarray(eli.LINE_COLOR)):
            next_move = [self.center_x-1, self.center_y-1]
        elif np.array_equal(self.map[self.center_x-1][self.center_y], np.asarray(eli.LINE_COLOR)):
            next_move = [self.center_x-1, self.center_y]
        elif np.array_equal(self.map[self.center_x-1][self.center_y+1], np.asarray(eli.LINE_COLOR)):
            next_move = [self.center_x-1, self.center_y+1]
        elif np.array_equal(self.map[self.center_x][self.center_y-1], np.asarray(eli.LINE_COLOR)):
            next_move = [self.center_x, self.center_y-1]
        elif np.array_equal(self.map[self.center_x][self.center_y+1], np.asarray(eli.LINE_COLOR)):
            next_move = [self.center_x, self.center_y+1]
        elif np.array_equal(self.map[self.center_x+1][self.center_y - 1], np.asarray(eli.LINE_COLOR)):
            next_move = [self.center_x+1, self.center_y - 1]
        elif np.array_equal(self.map[self.center_x+1][self.center_y], np.asarray(eli.LINE_COLOR)):
            next_move = [self.center_x+1, self.center_y]
        # elif np.array_equal(map[self.center_x+1][self.center_y + 1], np.asarray(eli.LINE_COLOR)):
        else:
            next_move = [self.center_x+1, self.center_y + 1]

        print(next_move)
        if len(next_move) != 0:
            # self.pacman = Label(self, image=self.render)
            # self.pacman.image = self.render
            self.pacman.place(x=next_move[0], y=next_move[1])




root = Tk()
app = Window(root)
root.wm_title("Tkinter window")
root.geometry("1197x734")
root.mainloop()
while True:
    time.sleep(0.1)
    app.move_pacman()
    root.mainloop()
