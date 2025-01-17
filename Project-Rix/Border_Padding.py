import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

class ImageBorderUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Border Processor")
        
        # Variables
        self.image_path = None
        self.original_image = None
        self.current_image = None
        self.padding = tk.IntVar(value=20)
        self.border_type = tk.StringVar(value="BORDER_REPLICATE")
        self.border_color = [255, 255, 255]  # Default white color
        
        # Border types mapping
        self.border_types = {
            "BORDER_REPLICATE": cv2.BORDER_REPLICATE,
            "BORDER_REFLECT": cv2.BORDER_REFLECT,
            "BORDER_REFLECT_101": cv2.BORDER_REFLECT_101,
            "BORDER_WRAP": cv2.BORDER_WRAP,
            "BORDER_CONSTANT": cv2.BORDER_CONSTANT
        }
        
        # Create UI elements
        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Upload button
        ttk.Button(main_frame, text="Upload Image", command=self.upload_image).grid(row=0, column=0, columnspan=2, pady=5)
        
        # Border type dropdown
        ttk.Label(main_frame, text="Border Type:").grid(row=1, column=0, pady=5)
        border_dropdown = ttk.Combobox(main_frame, 
                                     textvariable=self.border_type,
                                     values=list(self.border_types.keys()),
                                     state="readonly")
        border_dropdown.grid(row=1, column=1, pady=5)
        border_dropdown.bind('<<ComboboxSelected>>', self.update_image)
        
        # Padding slider
        ttk.Label(main_frame, text="Padding:").grid(row=2, column=0, pady=5)
        padding_slider = ttk.Scale(main_frame, 
                                 from_=0, to=100, 
                                 orient=tk.HORIZONTAL, 
                                 variable=self.padding,
                                 command=self.update_image)
        padding_slider.grid(row=2, column=1, pady=5)
        
        # Image display
        self.image_label = ttk.Label(main_frame)
        self.image_label.grid(row=4, column=0, columnspan=2, pady=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff")]
        )
        if file_path:
            self.image_path = file_path
            self.original_image = cv2.imread(file_path, cv2.IMREAD_COLOR)
            self.update_image()

    def choose_color(self):
        # Using a simple color chooser dialog
        color = tk.colorchooser.askcolor(title="Choose Border Color")
        if color[0]:  # color[0] contains RGB values
            self.border_color = [int(c) for c in color[0]]
            self.update_image()

    def update_image(self, *args):
        if self.original_image is not None:
            padding = self.padding.get()
            border_type = self.border_types[self.border_type.get()]
            
            # Apply border
            if border_type == cv2.BORDER_CONSTANT:
                bordered = cv2.copyMakeBorder(
                    self.original_image,
                    padding, padding, padding, padding,
                    border_type,
                    value=self.border_color
                )
            else:
                bordered = cv2.copyMakeBorder(
                    self.original_image,
                    padding, padding, padding, padding,
                    border_type
                )
            
            # Convert to RGB for display
            rgb_image = cv2.cvtColor(bordered, cv2.COLOR_BGR2RGB)
            
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
    app = ImageBorderUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()