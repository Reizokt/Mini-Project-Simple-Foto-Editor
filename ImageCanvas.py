import tkinter as tk
from tkinter import Canvas
import cv2
from PIL import Image, ImageTk
import numpy as np
class ImageCanvas(tk.Canvas):
    def __init__(self, master):
        self.width = 600
        self.height = 400
        Canvas.__init__(self, master=master, bg="white", width=self.width, height=self.height)
        self.shown_image = None
        self.ratio = 0
        self.rotation_degree = 0
        self.translate = (0,0)
        self.resize = (0,0)
        self.color_manipulation = (1,1,1)
        self.isGrayScale = False
        self.color_filters = []
        self.brightness = 1
        self.contrast = 1
        self.border = None
        self.padding = 0
        self.contrast_stretch = False

    def show_image(self, img=None):
        self.delete("all")
        image = img
        if img is None:
            print("No image to show")
            return
        if self.isGrayScale:
            image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if self.rotation_degree != 0:
            image = Image.fromarray(image).rotate(self.rotation_degree)
            image = np.array(image)
        height, width = image.shape[0], image.shape[1]
        if self.translate != (0,0):
            print(image)
            T = np.array([[1,0,self.translate[0]],[0,1,self.translate[1]]],dtype=np.float32)
            image = cv2.warpAffine(image, T, (width, height))
        if self.resize != (0,0):
            image = cv2.resize(image, (int(width*self.resize[0]), int(height*self.resize[1])))
            height, width = image.shape[0], image.shape[1]
        if self.color_manipulation != (1,1,1) and len(image.shape) == 3:
            image = np.clip(image * self.color_manipulation, 0, 255).astype(np.uint8)
        if self.contrast_stretch:
            image = self.contrast_stretching(image)
        if len(self.color_filters) > 0:
            for filter in self.color_filters:
                print("test2")
                if filter == "sepia":
                    # Sepia filter
                    print("test3")
                    kernel = np.array([[0.393, 0.769, 0.189],  # Red channel
                                    [0.349, 0.686, 0.168],  # Green channel
                                    [0.272, 0.534, 0.131]])  # Blue channel
                    image = cv2.transform(image, kernel)  # Apply sepia tone
                    image = cv2.convertScaleAbs(image, alpha=1, beta=35)  # Adjust brightness

                elif filter == "cyanotype":
                    # Cyanotype filter (emphasizing blue tones in RGB)
                    blue_channel_boost = np.zeros_like(image)
                    blue_channel_boost[..., 2] = 125  # Boost blue channel in RGB
                    image = cv2.add(image, blue_channel_boost)

                elif filter == "vignette":
                    # Vignette effect
                    rows, cols = image.shape[:2]
                    kernel_x = cv2.getGaussianKernel(cols, cols / 4)
                    kernel_y = cv2.getGaussianKernel(rows, rows / 4)
                    kernel = kernel_y @ kernel_x.T
                    mask = kernel / kernel.max()  # Normalize the mask
                    for i in range(3):  # Apply to all RGB channels
                        image[..., i] = image[..., i] * mask    
        image = cv2.convertScaleAbs(
                image,
                alpha=self.brightness,
                beta=50 * (self.contrast - 1)
            )
        if self.border != None:
            if self.border == cv2.BORDER_CONSTANT:
                image = cv2.copyMakeBorder(
                    image,
                    self.padding, self.padding, self.padding, self.padding,
                    self.border,
                    value=(0,0,0)
                )
            else:
                image = cv2.copyMakeBorder(
                    image,
                    self.padding, self.padding, self.padding, self.padding,
                    self.border
                )
        ratio = height / width
        new_width = width
        new_height = height

        if height>self.height or width > self.width:
            #Orientation is landscape
            if ratio<1:
                new_width = self.width
                new_height = int(new_width * ratio)
            #Portrait
            else:
                new_height = self.height
                new_width = int(new_height*width/height)
            self.shown_image = cv2.resize(image, (new_width, new_height))
            self.shown_image = ImageTk.PhotoImage(Image.fromarray(self.shown_image))
            self.ratio = height/new_height

            self.config(width=new_width, height=new_height) 
            self.create_image(new_width/2, new_height/2, anchor= tk.CENTER, image = self.shown_image)
            
    def save(self, path):
        image_array = ImageTk.getimage(self.shown_image)
        image_cv2 = np.array(image_array)
        if self.isGrayScale:
            image_cv2 = cv2.cvtColor(image_cv2, cv2.COLOR_RGB2GRAY)
        else:
            image_cv2 = cv2.cvtColor(image_cv2, cv2.COLOR_RGB2BGR)
        cv2.imwrite(path, image_cv2)
    
    def __repr__(self):
        return (
            f"{self.__class__.__name__}("+
            f"width={self.width}, "+
            f"height={self.height}, "+
            f"shown_image={self.shown_image}, "+
            f"ratio={self.ratio}, "+
            f"rotation_degree={self.rotation_degree}, "+
            f"translate={self.translate}, "+
            f"resize={self.resize}, "+
            f"color_manipulation={self.color_manipulation}, "+
            f"isGrayScale={self.isGrayScale}, "+
            f"color_filters={self.color_filters}"+
            ")"
        )
    def contrast_stretching(self, image):
        def helper(image):
            # Get the min and max pixel values
            R_min = np.min(image)
            R_max = np.max(image)
            # Desired output range (0 to 255)
            L_min = 0
            L_max = 255
            # Apply the contrast stretching formula
            stretched = ((image - R_min) / (R_max - R_min)) * (L_max - L_min) + L_min
            # Convert to uint8 type
            stretched = np.uint8(stretched)
            return stretched
        if self.isGrayScale:
            stretched = helper(image)
            return stretched
        else:
            stretched = np.zeros_like(image)
            for i in range(3):
                stretched[:,:,i] = helper(image[:,:,i])
            return stretched
            
            
