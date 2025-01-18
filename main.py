import tkinter as tk
import cv2
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from ImageCanvas import ImageCanvas
import numpy as np
image:np.ndarray = None
border_types = {
    "Border Replicate": cv2.BORDER_REPLICATE,
    "Border Reflect": cv2.BORDER_REFLECT,
    "Border Reflect 101": cv2.BORDER_REFLECT_101,
    "Border Wrap": cv2.BORDER_WRAP,
    "Border Constant": cv2.BORDER_CONSTANT,
    "None":None
}
root = tk.Tk()
style = ttk.Style()
style.theme_use("default")
style.configure("TButton", 
                foreground="white",
                background="#003066",
                font=("Arial", 12, "bold"),
                padding = (10,10,10,10),
                margin = (0,10,0,0)
                )
style.configure("TLabel",
                foreground = "white",
                background = "lightblue",
                font = ("Arial", 12, "bold"),
                margin = (0,10,0,0)
                )
style.configure("TScale",
                background = "lightblue",
                font = ("Arial", 12, "bold"),
                margin = (0,10,0,0),
                sliderthickness = 15,
                sliderlength= 10,
                troughrelief = "flat" 
                )
style.configure("TCheckbutton",
                foreground = "white",
                background = "lightblue",
                font = ("Arial", 12),
                margin = (0,10,0,0)
                )
style.configure("TRadiobutton",
                foreground = "white",
                background = "lightblue",
                font = ("Arial", 12),
                margin = (0,10,0,0)
                )
sepia = tk.BooleanVar()
cyanotype = tk.BooleanVar()
vignette = tk.BooleanVar()
compress_type = tk.StringVar()
root.state("zoomed")
root.title("Three Pane Layout")

def color_manipulation():
    global image
    canvas1.color_manipulation = (slider_color_red.get()/100, slider_color_green.get()/100, slider_color_blue.get()/100)
    canvas1.show_image(image)
def convertGrayScale():
    global image
    canvas1.isGrayScale = not canvas1.isGrayScale
    canvas1.show_image(image)
def importImageClick():
    global image
    filename = filedialog.askopenfilename(
    title="Select an Image File",
    filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),  # Include supported image formats
               ("All Files", "*.*")]  # Option to show all files
    )
    if filename:  # Check if a file was selected
        image = cv2.imread(filename)
        if image is not None:  # Check if the image was successfully read
            canvas1.show_image(image)
        else:
            print("Failed to load image. Please select a valid image file.")
    else:
        print("No file selected.")
def save():
    file_types = [
        ("PNG files", "*.png"),
        ("JPG files", "*.jpg"),
        ("All files", "*.*")
    ]
    path = None
    compression_type = compress_type.get()
    if compression_type == "None":
        pass    
    elif compression_type == "DCT":
        file_types.pop(0)
    else:
        file_types.pop(1)
    
    path = filedialog.asksaveasfilename(
    defaultextension=".png", 
    filetypes=file_types
    )
    if path:
        canvas1.save(path, compression_type)
def notOperation():
    global image
    image = cv2.bitwise_not(image)
    canvas1.show_image(image)

def onRotateChange(value):
    global image
    angle = int(value)
    canvas1.rotation_degree = angle
    canvas1.show_image(image)
    print(repr(canvas1))

def flipHorizontal():
    global image
    image = cv2.flip(image, 1)
    canvas1.show_image(image)

def flipVertical():
    global image
    image = cv2.flip(image, 0)
    canvas1.show_image(image)

def flipDiagonal():
    global image
    image = cv2.flip(image, 1)
    image = cv2.flip(image, 0)
    canvas1.show_image(image)

def translate(e):
    global image
    try:
        entry_x = entry_translatex.get() if entry_translatex.get() != "" else 0
        entry_y = entry_translatey.get() if entry_translatey.get() != "" else 0
        canvas1.translate = (int(entry_x), int(entry_y))
        canvas1.show_image(image)
    except ValueError:
        print("Invalid input for translate")

def scale(e):
    global image
    try:
        entry_x = entry_scalingx.get() if entry_scalingx.get() != "" else 100
        entry_y = entry_scalingy.get() if entry_scalingy.get() != "" else 100
        entry_x = int(entry_x)
        entry_y = int(entry_y)
        canvas1.resize = (entry_x/100, entry_y/100)
        canvas1.show_image(image)
    except ValueError:
        print("Invalid input for scale")

def color_filter():
    global image
    color_filters = canvas1.color_filters
    # Define the filters and their corresponding variables in a list
    filter_options = [
        ("sepia", sepia),
        ("cyanotype", cyanotype),
        ("vignette", vignette)
    ]

    # Iterate over the filters and update the color_filters list
    for filter_name, filter_var in filter_options:
        if filter_var.get() == 1 and filter_name not in color_filters:
            color_filters.append(filter_name)
        elif filter_var.get() == 0 and filter_name in color_filters:
            color_filters.remove(filter_name)

    # Update the canvas property
    canvas1.color_filters = color_filters
    canvas1.show_image(image)

def brightnessChange(event):
    global image
    brightness = event.widget.get()
    canvas1.brightness = float(brightness)
    canvas1.show_image(image)

def contrastChange(event):
    global image
    contrast = event.widget.get()
    canvas1.contrast = float(contrast)
    canvas1.show_image(image)
def borderChange(event):
    global image
    border = event.widget.get()
    canvas1.border = border_types[border]
    canvas1.show_image(image)

def paddingChange(event):
    global image
    padding = event.widget.get()
    canvas1.padding = int(padding)
    canvas1.show_image(image)
def contrast_stretching():
    canvas1.contrast_stretch = not canvas1.contrast_stretch
    canvas1.show_image(image)
def binaryOperation(operation):
    global image
    operations = {
            "AND": cv2.bitwise_and,
            "OR": cv2.bitwise_or,
            "XOR": cv2.bitwise_xor,
            "NOT": cv2.bitwise_not
        }
    if operation == "NOT":
        if image is None: return
        image = operations[operation](image)
        canvas1.show_image(image)
        return
    filename = filedialog.askopenfilename(
    title="Select the second Image File",
    filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),  # Include supported image formats
               ("All Files", "*.*")]  # Option to show all files
    )
    if filename:  # Check if a file was selected
        image2 = cv2.imread(filename)
        if image2 is not None:
            image2 = cv2.resize(image2, (image.shape[1], image.shape[0]))
            image = operations[operation](image, image2)
            canvas1.show_image(image)
        else:
            print("Failed to load image. Please select a valid image file.")
    else:
        print("No file selected.")
# Configure grid layout
root.grid_columnconfigure(0, weight=1)  # Left menu
root.grid_columnconfigure(1, weight=2)  # Canvas
root.grid_columnconfigure(2, weight=1)  # Right menu
root.grid_rowconfigure(0, weight=1)

# Create frames
frame1 = tk.Frame(root, background="lightblue", width=425, height=844)  # Left menu
frame2 = tk.Frame(root, background="white", width=850, height=844)     # Canvas (middle)
frame3 = tk.Frame(root, background="lightgreen", width=425, height=844) # Right menu

# Add frames to the grid
frame1.pack_propagate(False)
frame1.grid(row=0, column=0, sticky="nswe")
frame2.pack_propagate(False)
frame2.grid(row=0, column=1, sticky="nswe")
frame3.pack_propagate(False)
frame3.grid(row=0, column=2, sticky="nswe")

# Add sample widgets
ttk.Label(frame1, text="Left Menu", font=("Arial", 20, "bold")).pack(pady=10)
ttk.Label(frame2, text="Canvas Area", background="white").pack(pady=10)
ttk.Label(frame3, text="Right Menu", background="lightgreen").pack(pady=10)

canvas1 = ImageCanvas(frame2)
        

label1 = ttk.Label(frame2, text="Image 1", background="white")
label1.pack()
button = ttk.Button(frame2, text="Import Image", command=importImageClick)
button.pack()
canvas1.pack()
label_compress = ttk.Label(frame2, text="Compression type")
label_compress.pack()
frame_compress = tk.Frame(frame2, background="lightblue")
frame_compress.columnconfigure(0, weight=1, pad=10)
frame_compress.columnconfigure(1, weight=1, pad=10)
frame_compress.columnconfigure(2, weight=1, pad=10)
radio_compressNone = ttk.Radiobutton(frame_compress, text="None", variable=compress_type, value="None")
radio_compressNone.grid(column=0, row=0)
radio_compressDCT = ttk.Radiobutton(frame_compress, text="DCT", variable=compress_type, value="DCT")
radio_compressDCT.grid(column=1, row=0)
radio_compressRLE = ttk.Radiobutton(frame_compress, text="RLE", variable=compress_type, value="RLE")
radio_compressRLE.grid(column=2, row=0)
frame_compress.pack()
compress_type.set("None")

button_save = ttk.Button(frame2, text="Save", command=save)
button_save.pack()

ttk.Label(frame1, text="Image Effects").pack()
frame_image_effect = tk.Frame(frame1, background="lightblue")
frame_image_effect.columnconfigure(0, weight=1, pad=10)
frame_image_effect.columnconfigure(1, weight=1, pad=10)
frame_image_effect.columnconfigure(2, weight=1, pad=10)

button = ttk.Button(frame_image_effect, text="Gray scale",command=convertGrayScale)
button.grid(column=0, row=0)
button_negative = ttk.Button(frame_image_effect, text="Negative Transformation", command=notOperation)
button_negative.grid(column=1, row=0)
ttk.Button(frame_image_effect, text="Contrast stretching", command=contrast_stretching).grid(column=2, row=0)
frame_image_effect.pack()


label_rotate = ttk.Label(frame1, text="Rotate")
label_rotate_degree = ttk.Label(frame1, text="0°")
slider_rotate = ttk.Scale(frame1, from_=-180, to=180, orient="horizontal", command=lambda value: label_rotate_degree.config(text=f"Rotate: {float(value):.2f}°"))
label_rotate.pack()
label_rotate_degree.pack()
slider_rotate.pack()
slider_rotate.bind("<ButtonRelease-1>", lambda event: onRotateChange(slider_rotate.get()))


button_flipv_icon = ImageTk.PhotoImage(Image.open("icons/vertical_flip.png").resize((30,30)))
button_fliph_icon = ImageTk.PhotoImage(Image.open("icons/horizontal_flip.png").resize((30,30)))
button_flipd_icon = ImageTk.PhotoImage(Image.open("icons/diagonal_flip.png").resize((30,30)))

label_flip = ttk.Label(frame1, text="Flip", background="lightblue")
label_flip.pack()
container_flip = tk.Frame(frame1, background="lightblue")
button_fliph = ttk.Button(container_flip, image=button_fliph_icon, command=flipHorizontal)
button_fliph.grid(row=0, column=0)
button_flipv = ttk.Button(container_flip, image=button_flipv_icon, command=flipVertical)
button_flipv.grid(row=0, column=1)
button_flipd = ttk.Button(container_flip, image=button_flipd_icon, command=flipDiagonal)
button_flipd.grid(row=0, column=2)
container_flip.pack()


    

label_translate = ttk.Label(frame1, text="Translate", background="lightblue")
label_translate.pack()
container_translate = tk.Frame(frame1, background="lightblue")
label_translatex = ttk.Label(container_translate, text="X:")
label_translatex.pack(side="left", padx=10)
entry_translatex = tk.Entry(container_translate)
entry_translatex.bind("<Return>", translate)
entry_translatex.pack(side="left")
label_translatex2 = ttk.Label(container_translate, text="px")
label_translatex2.pack(side="left")
label_translatey = ttk.Label(container_translate, text="Y:")
label_translatey.pack(side="left", padx=10)
entry_translatey = tk.Entry(container_translate)
entry_translatey.bind("<Return>", translate)
entry_translatey.pack(side="left")
label_translatey2 = ttk.Label(container_translate, text="px")
label_translatey2.pack(side="left")
container_translate.pack()



label_scaling = ttk.Label(frame1, text="Scale", background="lightblue")
label_scaling.pack()
container_scaling = tk.Frame(frame1, background="lightblue")
label_scaling = ttk.Label(container_scaling, text="Scaling")
label_scaling.pack()
label_scalingx = ttk.Label(container_scaling, text="X:")
label_scalingx.pack(side="left", padx=10)
entry_scalingx = tk.Entry(container_scaling)
entry_scalingx.pack(side="left")
entry_scalingx.bind("<Return>", scale)
label_scalingx2 = ttk.Label(container_scaling, text="%")
label_scalingx2.pack(side="left")
label_scalingy = ttk.Label(container_scaling, text="Y:")
label_scalingy.pack(side="left", padx=10)
entry_scalingy = tk.Entry(container_scaling)
entry_scalingy.pack(side="left")
entry_scalingy.bind("<Return>", scale)
label_scalingy2 = ttk.Label(container_scaling, text="%")
label_scalingy2.pack(side="left")
container_scaling.pack()


label_color_manipulation = ttk.Label(frame1, text="Color Manipulation", background="lightblue")
label_color_manipulation.pack()

frame_color_manipulation = tk.Frame(frame1, background="lightblue")
frame_color_manipulation.grid_columnconfigure(0, weight=1, pad=10)
frame_color_manipulation.grid_columnconfigure(1, weight=1, pad=10)
frame_color_manipulation.grid_columnconfigure(2, weight=1, pad=10)


label_color_red = ttk.Label(frame_color_manipulation, text="Red: 100")
label_color_red.grid(row=0, column=0)
slider_color_red = ttk.Scale(frame_color_manipulation, from_=0, to=200, orient="horizontal", command=lambda value: label_color_red.config(text=f"Red: {float(value):.0f}"))
slider_color_red.grid(row=1, column=0)
label_color_green = ttk.Label(frame_color_manipulation, text="Green: 100")
label_color_green.grid(row=0, column=1)
slider_color_green = ttk.Scale(frame_color_manipulation, from_=0, to=200, orient="horizontal", command=lambda value: label_color_green.config(text=f"Green: {float(value):.0f}"))
slider_color_green.grid(row=1, column=1)
label_color_blue = ttk.Label(frame_color_manipulation, text="Blue: 100")
label_color_blue.grid(row=0, column=2)
slider_color_blue = ttk.Scale(frame_color_manipulation, from_=0, to=200, orient="horizontal", command=lambda value: label_color_blue.config(text=f"Blue: {float(value):.0f}"))
slider_color_blue.grid(row=1, column=2)
frame_color_manipulation.pack()
label_brightness = ttk.Label(frame1, text="Brightness: 1.0")
brightness_slider = ttk.Scale(frame1, 
                            from_=0.1, to=3.0, 
                            orient=tk.HORIZONTAL, command=lambda value: label_brightness.config(text=f"Brightness: {float(value):.1f}"))
brightness_slider.bind("<ButtonRelease-1>", brightnessChange)
brightness_slider.set(1.0)
label_brightness.pack()
brightness_slider.pack()
        
# Contrast slider
label_contrast = ttk.Label(frame1, text="Contrast:")
contrast_slider = ttk.Scale(frame1, 
                            from_=0.1, to=3.0, 
                            orient=tk.HORIZONTAL, command=lambda value: label_contrast.config(text=f"Contrast: {float(value):.1f}"))
contrast_slider.set(1.0)
contrast_slider.bind("<ButtonRelease-1>", contrastChange)
label_contrast.pack()
contrast_slider.pack()
label_color_filter = ttk.Label(frame1, text="Color Filter", background="lightblue")
label_color_filter.pack()
frame_filter = tk.Frame(frame1, background="lightblue")
frame_filter.columnconfigure(0, weight=1, pad=10)
frame_filter.columnconfigure(1, weight=1, pad=10)
frame_filter.columnconfigure(2, weight=1, pad=10)
checkbox_sepia = ttk.Checkbutton(frame_filter, text="Sepia", onvalue=1, offvalue=0, variable=sepia)
checkbox_cyanotype = ttk.Checkbutton(frame_filter, text="Cyanotype", onvalue=1, offvalue=0, variable=cyanotype)
checkbox_vignette = ttk.Checkbutton(frame_filter, text="Vignette", onvalue=1, offvalue=0, variable=vignette)
for i, checkbox in enumerate([checkbox_sepia, checkbox_cyanotype, checkbox_vignette]):
    checkbox.configure(command=lambda: color_filter())
    checkbox.grid(row=0, column=i)
frame_filter.pack()

for i in [slider_color_red, slider_color_green, slider_color_blue]:
    i.set(100)
    i.bind("<ButtonRelease-1>", lambda e: color_manipulation())
ttk.Label(frame1, text="Border Type:").pack()
border_dropdown = ttk.Combobox(frame1,
                            values=list(border_types.keys()),
                            state="readonly")
border_dropdown.set("None")
border_dropdown.pack()
border_dropdown.bind('<<ComboboxSelected>>', borderChange)

# Padding slider
ttk.Label(frame1, text="Padding:").pack()
padding_slider = ttk.Scale(frame1, 
                        from_=0, to=100, 
                        orient=tk.HORIZONTAL)
padding_slider.bind("<ButtonRelease-1>", paddingChange)
padding_slider.pack()



ttk.Label(frame3, text="Binary Operation", background="lightgreen").pack()

frame_binary = ttk.Frame(frame3)
frame_binary.columnconfigure(0, weight=1)
frame_binary.columnconfigure(1, weight=1)
frame_binary.columnconfigure(2, weight=1)
frame_binary.columnconfigure(3, weight=1)

ttk.Button(frame_binary, text="AND", command=lambda : binaryOperation("AND")).grid(column=0, row=0)
ttk.Button(frame_binary, text="OR", command=lambda : binaryOperation("OR")).grid(column=1, row=0)
ttk.Button(frame_binary, text="XOR", command=lambda : binaryOperation("XOR")).grid(column=2, row=0)
ttk.Button(frame_binary, text="NOT", command=lambda : binaryOperation("NOT")).grid(column=3, row=0)
frame_binary.pack()

root.mainloop()
