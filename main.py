import tkinter as tk
import cv2
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from ImageCanvas import ImageCanvas
import numpy as np
from sklearn.cluster import KMeans
image:np.ndarray = None
crop = False
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
style.configure(
    "TCombobox",
    foreground="black",  # Text color
    background="lightblue",  # Background of the entry field
    font=("Arial", 20, "bold"),
    padding = (10,10,10,10),
    margin = (0,10,0,0)
)
# Configure the dropdown list
style.map(
    "TCombobox",
    fieldbackground=[("readonly", "lightblue")],  # Background of the entry field (readonly)
    background=[("readonly", "lightblue")], 
    foreground=[("readonly", "white")]# Background of the dropdown menu
)
sepia = tk.BooleanVar()
cyanotype = tk.BooleanVar()
vignette = tk.BooleanVar()
compress_type = tk.StringVar()
root.state("zoomed")
root.title("Three Pane Layout")
def overlayChange(e):
    canvas.image_overlay_alpha = overlay_slider_alpha.get()
    canvas.image_overlay_position = (overlay_slider_x.get(), overlay_slider_y.get())
    canvas.show_image(image)
def change_crop_state():
    global crop
    crop = not crop
def color_manipulation():
    global image
    canvas.color_manipulation = (slider_color_red.get()/100, slider_color_green.get()/100, slider_color_blue.get()/100)
    canvas.show_image(image)
def convertGrayScale():
    global image
    canvas.isGrayScale = not canvas.isGrayScale
    canvas.show_image(image)
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
            canvas.show_image(image)
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
        canvas.save(path, compression_type)
def notOperation():
    global image
    image = cv2.bitwise_not(image)
    canvas.show_image(image)

def onRotateChange(value):
    global image
    angle = int(value)
    canvas.rotation_degree = angle
    canvas.show_image(image)
    print(repr(canvas))

def flipHorizontal():
    global image
    image = cv2.flip(image, 1)
    canvas.show_image(image)

def flipVertical():
    global image
    image = cv2.flip(image, 0)
    canvas.show_image(image)

def flipDiagonal():
    global image
    image = cv2.flip(image, 1)
    image = cv2.flip(image, 0)
    canvas.show_image(image)

def translate(e):
    global image
    try:
        entry_x = entry_translatex.get() if entry_translatex.get() != "" else 0
        entry_y = entry_translatey.get() if entry_translatey.get() != "" else 0
        canvas.translate = (int(entry_x), int(entry_y))
        canvas.show_image(image)
    except ValueError:
        print("Invalid input for translate")

def scale(e):
    global image
    try:
        entry_x = entry_scalingx.get() if entry_scalingx.get() != "" else 100
        entry_y = entry_scalingy.get() if entry_scalingy.get() != "" else 100
        entry_x = int(entry_x)
        entry_y = int(entry_y)
        canvas.resize = (entry_x/100, entry_y/100)
        canvas.show_image(image)
    except ValueError:
        print("Invalid input for scale")

def color_filter():
    global image
    color_filters = canvas.color_filters
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
    canvas.color_filters = color_filters
    canvas.show_image(image)

def brightnessChange(event):
    global image
    brightness = event.widget.get()
    canvas.brightness = float(brightness)
    canvas.show_image(image)

def contrastChange(event):
    global image
    contrast = event.widget.get()
    canvas.contrast = float(contrast)
    canvas.show_image(image)
def borderChange(event):
    global image
    border = event.widget.get()
    canvas.border = border_types[border]
    canvas.show_image(image)
def paddingChange(event):
    global image
    padding = event.widget.get()
    canvas.padding = int(padding)
    canvas.show_image(image)
def contrast_stretching():
    canvas.contrast_stretch = not canvas.contrast_stretch
    canvas.show_image(image)
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
        canvas.show_image(image)
        return
    filename = filedialog.askopenfilename(
    title="Select the second Image File",
    filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),  # Include supported image formats
               ("All Files", "*.*")]  # Option to show all files
    )
    if filename:
        image2 = cv2.imread(filename)
        if operation == "BLEND":
            canvas.image_blend = image2
            canvas.show_image(image)
            label_blend.pack(after=frame_binary)
            alpha_slider.pack(after=label_blend)
            return
        elif operation == "MATCH":
            if canvas.image_match is None:
                label_canvas2.pack()
                canvas2.pack()
            canvas.image_match = image2
            canvas2.show_image(canvas.image_match)
            canvas.show_image(image)
        elif operation == "TEMPLATE":
            label_canvas2.pack()
            canvas2.pack()
            canvas.image_template = image2
            canvas2.show_image(image2)
            canvas.show_image(image)
        elif operation == "OVERLAY":
            canvas.image_overlay = image2
            label_overlay.pack(after=frame_binary)
            overlay_slider_alpha.pack(after=label_overlay)
            label_overlay_x.pack(after=overlay_slider_alpha)
            overlay_slider_x.pack(after=label_overlay_x)
            label_overlay_y.pack(after=overlay_slider_x)
            overlay_slider_y.pack(after=label_overlay_y)
            canvas.image_overlay_position= (overlay_slider_x.get(), overlay_slider_y.get())
            canvas.image_overlay_alpha = overlay_slider_alpha.get()
            canvas.show_image(image)
        elif image2 is not None:
            image2 = cv2.resize(image2, (image.shape[1], image.shape[0]))
            image = operations[operation](image, image2)
            canvas.show_image(image)
        else:
            print("Failed to load image. Please select a valid image file.")
    else:
        print("No file selected.")
def start_crop(event):
    global start_x, start_y, rect_id, crop
    if not crop : return
    start_x, start_y = event.x, event.y
    rect_id = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="red")

def draw_crop(event):
    global rect_id, crop
    if not crop : return
    if rect_id:
        canvas.coords(rect_id, start_x, start_y, event.x, event.y)

def end_crop(event):
    global start_x, start_y, image, crop
    if not crop : return
    if rect_id and image is not None:
        # Get canvas coordinates of the cropping rectangle
        x1, y1, x2, y2 = canvas.coords(rect_id)
        
        # Convert canvas coordinates to image coordinates by accounting for canvas scaling
        scale_x = image.shape[1] / canvas.winfo_width()  # Scaling factor for x
        scale_y = image.shape[0] / canvas.winfo_height()  # Scaling factor for y
        
        # Adjust coordinates based on scaling
        x1, y1, x2, y2 = int(x1 * scale_x), int(y1 * scale_y), int(x2 * scale_x), int(y2 * scale_y)
        # Ensure coordinates are within image bounds
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(image.shape[1], x2), min(image.shape[0], y2)

        if x1 < x2 and y1 < y2:
            print(image)
            image = canvas.getTransformedImage()[y1:y2, x1:x2]
            canvas.show_image(image)
            resetTransformations()
            crop = not crop
        else:
            print("Invalid crop area. Please try again.")
def resetTransformations():
    global image
    canvas.resetTransformation()
    entry_translatex.delete(0, tk.END)
    entry_translatey.delete(0, tk.END)
    entry_scalingx.delete(0, tk.END)
    entry_scalingy.delete(0, tk.END)
    slider_rotate.set(0)
    alpha_slider.set(0.5)
    label_blend.pack_forget()
    alpha_slider.pack_forget()

    label_overlay.pack_forget()
    overlay_slider_alpha.pack_forget()
    overlay_slider_alpha.set(1)
    label_overlay_x.pack_forget()
    overlay_slider_x.pack_forget()
    overlay_slider_x.set(0)
    label_overlay_y.pack_forget()
    overlay_slider_y.pack_forget()
    overlay_slider_y.set(0)
    canvas.show_image(image)

def alphaChange(event):
    global image
    canvas.image_blend_alpha = event.widget.get()
    canvas.show_image(image)

def fourier_transform():
    global image, rotated_image
    if image is None:
        print("No image to transform. Please import an image first.")
        return
    
    try:
        # Get the selection (FFT or DFT)
        transform_type = select_box_fourier.get()
        
        # Convert the image to grayscale for simplicity in Fourier Transform
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        if transform_type == "FFT":
            f_transform = np.fft.fft2(gray_image)
            f_shift = np.fft.fftshift(f_transform)  # Center the low frequencies
            image = 20 * np.log(np.abs(f_shift))
            
            
        elif transform_type == "DFT":
            dft = cv2.dft(np.float32(gray_image), flags=cv2.DFT_COMPLEX_OUTPUT)
            dft_shift = np.fft.fftshift(dft)
            image = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))
        
        else:
            print("Invalid transform type selected.")
            return
        
        # Normalize and display the result
        normalized_spectrum = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        image = cv2.cvtColor(normalized_spectrum, cv2.COLOR_GRAY2BGR)
        canvas.show_image(image)
    except Exception as e:
        print(f"An error occurred during Fourier Transform: {e}")
def apply_blur_filter():
    global image
    canvas.blur_filter = select_box_blur.get()
    canvas.show_image(image)

def applyEdgeDetection():
    global image
    edge_detection = select_box_edge.get()
    canvas.edge_detection = edge_detection
    canvas.show_image(image)
def apply_histogram_equalization():
    global image
    canvas.histogram = not canvas.histogram
    canvas.show_image(image)
def applySegmentation():
    global image
    segmentation = select_box_segmentation.get()
    if segmentation == "K-means":
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        pixels = image.reshape((-1, 1))  # Each pixel is a 1D vector (grayscale intensity)
        kmeans = KMeans(n_clusters=2, random_state=0).fit(pixels)  # We choose k=2 for simplicity
        Kmean_image = kmeans.labels_.reshape(image.shape)
        kmeans_image = (Kmean_image * 255).astype(np.uint8)
        image = kmeans_image
        canvas.show_image(image)
    if segmentation =="Thresholding":
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresholded_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        image = thresholded_image
        canvas.show_image(image)

def applyRestore(method):
    restorations = canvas.restoration
    if method not in restorations:
        restorations.append(method)
    else:
        restorations.remove(method)
    canvas.restoration = restorations
    canvas.show_image(image)

def gammaChange(event):
    global image
    gamma = event.widget.get()
    canvas.gamma = float(gamma)
    canvas.show_image(image)
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

canvas = ImageCanvas(frame2)
        

label1 = ttk.Label(frame2, text="Image", background="white", font=("Arial", 12, "bold"), foreground="black")
label1.pack()
button = ttk.Button(frame2, text="Import Image", command=importImageClick)
button.pack()
canvas.bind("<ButtonPress-1>", start_crop)
canvas.bind("<B1-Motion>", draw_crop)
canvas.bind("<ButtonRelease-1>", end_crop)
canvas.pack()
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
label_gamma = ttk.Label(frame1, text="Gamma: 1.0")
gamma_slider = ttk.Scale(frame1,
                        from_=0.1, to=3.0,
                        orient=tk.HORIZONTAL, command=lambda value: label_gamma.config(text=f"Gamma: {float(value):.1f}"))
gamma_slider.bind("<ButtonRelease-1>", gammaChange)
gamma_slider.set(1.0)
label_gamma.pack()
gamma_slider.pack()


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
ttk.Button(frame_binary, text="BLEND", command=lambda : binaryOperation("BLEND")).grid(column=0, row=1, columnspan=2, sticky="nsew")
ttk.Button(frame_binary, text="Overlay", command=lambda : binaryOperation("OVERLAY")).grid(column=2, row=1, columnspan=2, sticky="nsew")
label_blend = ttk.Label(frame3, text="Image Blend Alpha: 0.5")
label_blend.pack_forget()
alpha_slider = ttk.Scale(frame3, 
                        from_=0, to=1,
                        orient=tk.HORIZONTAL, command=lambda e: label_blend.config(text = f"Image Blend Alpha: {float(e):.2f}"))
alpha_slider.bind("<ButtonRelease-1>", alphaChange)
alpha_slider.set(0.5)
alpha_slider.pack_forget()

label_overlay = ttk.Label(frame3, text="Image overlay Alpha: 1")
label_overlay.pack_forget()
overlay_slider_alpha = ttk.Scale(frame3, 
                        from_=0, to=1,
                        orient=tk.HORIZONTAL, command=lambda e: label_overlay.config(text = f"Image overlay Alpha: {float(e):.2f}"))
overlay_slider_alpha.bind("<ButtonRelease-1>", overlayChange)
overlay_slider_alpha.set(1)
overlay_slider_alpha.pack_forget()
label_overlay_x = ttk.Label(frame3, text="Overlay X: 0")
label_overlay_x.pack_forget()
overlay_slider_x = ttk.Scale(frame3,
                        from_=0, to=1,
                        orient=tk.HORIZONTAL, command=lambda e: label_overlay_x.config(text = f"Overlay X: {float(e):.2f}"))
overlay_slider_x.bind("<ButtonRelease-1>", overlayChange)
overlay_slider_x.set(0)
overlay_slider_x.pack_forget()
label_overlay_y = ttk.Label(frame3, text="Overlay Y: 0")
label_overlay_y.pack_forget()
overlay_slider_y = ttk.Scale(frame3,
                        from_=0, to=1,
                        orient=tk.HORIZONTAL, command=lambda e: label_overlay_y.config(text = f"Overlay Y: {float(e):.2f}"))
overlay_slider_y.bind("<ButtonRelease-1>", overlayChange)
overlay_slider_y.set(0)
overlay_slider_y.pack_forget()



ttk.Label(frame3, text="Toggle crop", background="lightgreen").pack()
button_crop = ttk.Button(frame3, text="Crop", command=change_crop_state)
button_crop.pack()
ttk.Label(frame3, text="Fourier Transform", background="lightgreen").pack()
frame_fourier = tk.Frame(frame3, background="lightgreen")
frame_fourier.columnconfigure(0, weight=1, pad=10)
frame_fourier.columnconfigure(1, weight=1, pad=10)
select_box_fourier = ttk.Combobox(frame_fourier,
                            values=["FFT", "DFT"],
                            state="readonly")
select_box_fourier.set("FFT")
select_box_fourier.grid(column=0, row=0)
button_fourier = ttk.Button(frame_fourier, text="Apply", command=fourier_transform)
button_fourier.grid(column=1, row=0)
frame_fourier.pack()
ttk.Label(frame3, text="Spatial Filter", background="lightgreen").pack()
frame_blur = tk.Frame(frame3, background="lightgreen")
frame_blur.columnconfigure(0, weight=1, pad=10)
frame_blur.columnconfigure(1, weight=1, pad=10)
select_box_blur = ttk.Combobox(frame_blur,
                            values=["Mean Filter", "Gaussian Filter", "Median Filter","None"],
                            state="readonly")
select_box_blur.set("Mean Filter")
select_box_blur.grid(column=0, row=0)
button_blur = ttk.Button(frame_blur, text="Apply", command=apply_blur_filter)
button_blur.grid(column=1, row=0)
frame_blur.pack()

ttk.Label(frame3, text="Edge Detection", background="lightgreen").pack()
frame_edge = tk.Frame(frame3, background="lightgreen")
frame_edge.columnconfigure(0, weight=1, pad=10)
frame_edge.columnconfigure(1, weight=1, pad=10)
select_box_edge = ttk.Combobox(frame_edge,
                            values=["Sobel", "Laplacian", "Canny", "None"],
                            state="readonly")
select_box_edge.set("Sobel")
select_box_edge.grid(column=0, row=0)
button_edge = ttk.Button(frame_edge, text="Apply", command= applyEdgeDetection)
button_edge.grid(column=1, row=0)
frame_edge.pack()

button_histogram = ttk.Button(frame3, text="Histogram Equalization", command=apply_histogram_equalization)
button_histogram.pack()

frame_segmentation = tk.Frame(frame3, background="lightgreen")
frame_segmentation.columnconfigure(0, weight=1, pad=10)
frame_segmentation.columnconfigure(1, weight=1, pad=10)
select_box_segmentation = ttk.Combobox(frame_segmentation,
                            values=["K-means", "Thresholding"],
                            state="readonly")
select_box_segmentation.set("K-means")
select_box_segmentation.grid(column=0, row=0)
button_segmentation = ttk.Button(frame_segmentation, text="Apply", command=applySegmentation)
button_segmentation.grid(column=1, row=0)
frame_segmentation.pack()

label_image_restoration = ttk.Label(frame3, text="Image Restoration", background="lightgreen")
label_image_restoration.pack()
frame_image_restoration = tk.Frame(frame3, background="lightgreen")
frame_image_restoration.columnconfigure(0, weight=1, pad=10)
frame_image_restoration.columnconfigure(1, weight=1, pad=10)
frame_image_restoration.columnconfigure(2, weight=1, pad=10)

button_wiener = ttk.Button(frame_image_restoration, text="Wiener", command=lambda : applyRestore("Wiener"))
button_wiener.grid(column=0, row=0)
button_gaussian = ttk.Button(frame_image_restoration, text="Gaussian", command=lambda : applyRestore("Gaussian"))
button_gaussian.grid(column=1, row=0)
button_median = ttk.Button(frame_image_restoration, text="Inpainting", command=lambda : applyRestore("Inpainting"))
button_median.grid(column=2, row=0)
frame_image_restoration.pack()
ttk.Label(frame3, text="Morphological operations", background="lightgreen").pack()

frame_morph = ttk.Frame(frame3)
frame_morph.columnconfigure(0, weight=1)
frame_morph.columnconfigure(1, weight=1)
frame_morph.columnconfigure(2, weight=1)

def imageMorph(operation):
    morphs = canvas.image_morph
    if operation not in morphs:
        morphs.append(operation)
    else:
        morphs.remove(operation)
    canvas.image_morph = morphs
    canvas.show_image(image)
ttk.Button(frame_morph, text="Dilation", command=lambda : imageMorph("Dilation")).grid(column=0, row=0, sticky="nsew")
ttk.Button(frame_morph, text="Erosion", command=lambda : imageMorph("Erosion")).grid(column=1, row=0, sticky="nsew")
ttk.Button(frame_morph, text="Opening", command=lambda : imageMorph("Opening")).grid(column=2, row=0, sticky="nsew")
ttk.Button(frame_morph, text="Closing", command=lambda : imageMorph("Closing")).grid(column=0, row=1)
ttk.Button(frame_morph, text="Extract Boundary", command=lambda : imageMorph("Boundary Extraction")).grid(column=1, row=1)
ttk.Button(frame_morph, text="Skeletonize", command=lambda : imageMorph("Skeletonize")).grid(column=2, row=1)
frame_morph.pack()
ttk.Button(frame3, text="Match Image", command=lambda:binaryOperation("MATCH")).pack()
label_canvas2 = ttk.Label(frame2, text="Image 2", background="white", foreground="black")
canvas2 = ImageCanvas(frame2)
ttk.Button(frame3, text="Match Template", command=lambda:binaryOperation("TEMPLATE")).pack()
root.mainloop()