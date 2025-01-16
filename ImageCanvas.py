import tkinter as tk
from tkinter import Canvas
import cv2
from tkinter import filedialog
from PIL import Image, ImageTk
class ImageCanvas(tk.Canvas):
    def __init__(self, master):
        Canvas.__init__(self, master=master, bg="white", width=600, height=400)
        self.shown_image = None
        self.ratio = 0

    def show_image(self, img=None):
        self.delete("all")
        if img is None: print("Error")
        image = None

        if len(img.shape) == 2:image =img
        else: image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        height, width = image.shape[0], image.shape[1]
        ratio = height / width
        new_width = width
        new_height = height

        if height>self.winfo_height() or width > self.winfo_width():
            #Orientation is landscape
            if ratio<1:
                new_width = self.winfo_width()
                new_height = int(new_width * ratio)
            #Portrait
            else:
                new_height = self.winfo_height()
                new_width = int(new_height*width/height)
            self.shown_image = cv2.resize(image, (new_width, new_height))
            self.shown_image = ImageTk.PhotoImage(Image.fromarray(self.shown_image))
            self.ratio = height/new_height

            self.config(width=new_width, height=new_height)
            self.create_image(new_width/2, new_height/2, anchor= tk.CENTER, image = self.shown_image)
            


