import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

class ImageProcessorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        
        # Variables
        self.image_path = None
        self.original_image = None
        self.current_image = None
        self.brightness_value = tk.DoubleVar(value=1.0)
        self.contrast_value = tk.DoubleVar(value=1.0)
        
        # Create UI elements
        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Upload button
        ttk.Button(main_frame, text="Upload Image", command=self.upload_image).grid(row=0, column=0, pady=5)
        
        # Image display
        self.image_label = ttk.Label(main_frame)
        self.image_label.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Brightness slider
        ttk.Label(main_frame, text="Brightness:").grid(row=2, column=0, pady=5)
        brightness_slider = ttk.Scale(main_frame, 
                                    from_=0.1, to=3.0, 
                                    orient=tk.HORIZONTAL, 
                                    variable=self.brightness_value,
                                    command=self.update_image)
        brightness_slider.grid(row=2, column=1, pady=5)
        
        # Contrast slider
        ttk.Label(main_frame, text="Contrast:").grid(row=3, column=0, pady=5)
        contrast_slider = ttk.Scale(main_frame, 
                                  from_=0.1, to=3.0, 
                                  orient=tk.HORIZONTAL, 
                                  variable=self.contrast_value,
                                  command=self.update_image)
        contrast_slider.grid(row=3, column=1, pady=5)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff")]
        )
        if file_path:
            self.image_path = file_path
            self.original_image = cv2.imread(file_path)
            self.update_image()

    def update_image(self, *args):
        if self.original_image is not None:
            # Apply brightness and contrast adjustments
            adjusted = cv2.convertScaleAbs(
                self.original_image,
                alpha=self.brightness_value.get(),
                beta=50 * (self.contrast_value.get() - 1)
            )
            
            # Convert to RGB for display
            rgb_image = cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)
            
            # Resize image if too large
            max_size = 500
            height, width = rgb_image.shape[:2]
            if height > max_size or width > max_size:
                scale = max_size / max(height, width)
                new_width = int(width * scale)
                new_height = int(height * scale)
                rgb_image = cv2.resize(rgb_image, (new_width, new_height))
            
            # Convert to PhotoImage for display
            image = Image.fromarray(rgb_image)
            photo = ImageTk.PhotoImage(image)
            
            # Update display
            self.image_label.configure(image=photo)
            self.image_label.image = photo  # Keep a reference!

def main():
    root = tk.Tk()
    app = ImageProcessorUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()