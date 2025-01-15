import tkinter as tk
import cv2
from tkinter import filedialog

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

#Frame 1
button = tk.Button(frame1, text="Import Image")
def importImageClick(event):
    filename = filedialog.askopenfilename(
    title="Select an Image File",
    filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),  # Include supported image formats
               ("All Files", "*.*")]  # Option to show all files
    )
    cv2.imread(filename)
button.bind("<ButtonRelease>", importImageClick)
button.pack()
root.mainloop()
