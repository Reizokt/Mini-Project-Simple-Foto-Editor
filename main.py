import tkinter as tk
import cv2
from tkinter import filedialog
from PIL import Image, ImageTk
from ImageCanvas import ImageCanvas
import numpy as np
import os

image:np.ndarray = None
root = tk.Tk()
root.geometry("1700x844")
root.title("Three Pane Layout")

# Configure grid layout
root.grid_columnconfigure(0, weight=1)  # Left menu
root.grid_columnconfigure(1, weight=3)  # Canvas
root.grid_columnconfigure(2, weight=1)  # Right menu

# Create frames
frame1 = tk.Frame(root, bg="lightblue", width=200, height=844)  # Left menu
frame2 = tk.Frame(root, bg="white", width=1000, height=844)     # Canvas (middle)
frame3 = tk.Frame(root, bg="lightgreen", width=200, height=844) # Right menu

# Add frames to the grid
frame1.grid(row=0, column=0, sticky="nswe")
frame2.grid(row=0, column=1, sticky="nswe")
frame3.grid(row=0, column=2, sticky="nswe")

# Add sample widgets
tk.Label(frame1, text="Left Menu", bg="lightblue").pack(pady=10)
tk.Label(frame2, text="Canvas Area", bg="white").pack(pady=10)
tk.Label(frame3, text="Right Menu", bg="lightgreen").pack(pady=10)

tk.Scale(frame1, from_=0, to=100, orient="horizontal").pack(pady=10)

canvas1 = ImageCanvas(frame2)
#Frame 1
def importImageClick():
    global image
    my_directory = os.path.dirname(os.path.abspath(__file__))
    filename = filedialog.askopenfilename(
    title="Select an Image File",initialdir=my_directory,
    filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),  # Include supported image formats
               ("All Files", "*.*")]  # Option to show all files
    )
    image = cv2.imread(filename)
    if filename:  # Check if a file was selected
        image = cv2.imread(filename)
        if image is not None:  # Check if the image was successfully read
            canvas1.show_image(image)
        else:
            print("Failed to load image. Please select a valid image file.")
        filename.close()
    else:
        print("No file selected.")
        

label1 = tk.Label(frame2, text="Image 1", background="white")
label1.pack()
button = tk.Button(frame2, text="Import Image", command=importImageClick)
button.pack()
canvas1.pack()


def convertGrayScale():
    global image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    canvas1.show_image(image)
button = tk.Button(frame1, text="Gray scale",command=convertGrayScale)
button.pack()

def save():
    global image
    my_directory = os.path.dirname(os.path.abspath(__file__))
    filename = filedialog.asksaveasfilename(
        title="Save image file",
        initialdir=my_directory,
        initialfile="jogi ganteng.jpg",
        filetypes=[("Image Files", "*.jpg;"),  # Include supported image formats
                   ("All Files", "*.*")]  # Option to show all files
    )
    if filename:
        cv2.imwrite(filename, image)
    
    
button_save = tk.Button(frame1, text="Save", command=save)
button_save.pack()

def notOperation():
    global image
    image = cv2.bitwise_not(image)
    canvas1.show_image(image)

button_negative = tk.Button(frame1, text="Negative Transformation", command=notOperation)
button_negative.pack()
root.mainloop()
