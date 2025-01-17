import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

class BitwiseOperationsUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bitwise Operations")
        
        # Variables
        self.image1_path = None
        self.image2_path = None
        self.image1 = None
        self.image2 = None
        self.operation = tk.StringVar(value="AND")
        
        # Operations mapping
        self.operations = {
            "AND": cv2.bitwise_and,
            "OR": cv2.bitwise_or,
            "XOR": cv2.bitwise_xor,
            "NOT": cv2.bitwise_not
        }
        
        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Image 1 section
        ttk.Label(main_frame, text="Image 1").grid(row=0, column=0, pady=5)
        ttk.Button(main_frame, text="Upload Image 1", 
                  command=lambda: self.upload_image(1)).grid(row=1, column=0, pady=5)
        self.image1_label = ttk.Label(main_frame)
        self.image1_label.grid(row=2, column=0, padx=10, pady=5)
        
        # Operation selection (center)
        ttk.Label(main_frame, text="Operation:").grid(row=1, column=1, pady=5)
        operation_dropdown = ttk.Combobox(main_frame, 
                                        textvariable=self.operation,
                                        values=list(self.operations.keys()),
                                        state="readonly")
        operation_dropdown.grid(row=2, column=1, pady=5)
        operation_dropdown.bind('<<ComboboxSelected>>', self.perform_operation)
        
        # Image 2 section
        ttk.Label(main_frame, text="Image 2").grid(row=0, column=2, pady=5)
        self.image2_button = ttk.Button(main_frame, text="Upload Image 2", 
                                      command=lambda: self.upload_image(2))
        self.image2_button.grid(row=1, column=2, pady=5)
        self.image2_label = ttk.Label(main_frame)
        self.image2_label.grid(row=2, column=2, padx=10, pady=5)
        
        # Result section
        ttk.Label(main_frame, text="Result").grid(row=3, column=0, columnspan=3, pady=5)
        self.result_label = ttk.Label(main_frame)
        self.result_label.grid(row=4, column=0, columnspan=3, pady=5)
        
        # Save button
        self.save_button = ttk.Button(main_frame, text="Save Result", 
                                    command=self.save_result, state='disabled')
        self.save_button.grid(row=5, column=0, columnspan=3, pady=10)

    def upload_image(self, image_num):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff")]
        )
        if file_path:
            if image_num == 1:
                self.image1_path = file_path
                self.image1 = cv2.imread(file_path)
                self.display_image(self.image1, self.image1_label)
            else:
                self.image2_path = file_path
                self.image2 = cv2.imread(file_path)
                self.display_image(self.image2, self.image2_label)
            
            # Enable/disable Image 2 upload based on operation
            self.update_ui_state()
            
            # Perform operation if both images are loaded (or one for NOT)
            self.perform_operation()

    def display_image(self, image, label, max_size=200):
        if image is not None:
            # Convert to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Resize image if too large
            height, width = rgb_image.shape[:2]
            if height > max_size or width > max_size:
                scale = max_size / max(height, width)
                new_width = int(width * scale)
                new_height = int(height * scale)
                rgb_image = cv2.resize(rgb_image, (new_width, new_height))
            
            # Convert to PhotoImage
            image = Image.fromarray(rgb_image)
            photo = ImageTk.PhotoImage(image)
            
            # Update label
            label.configure(image=photo)
            label.image = photo

    def update_ui_state(self):
        # Enable/disable Image 2 upload based on operation
        if self.operation.get() == "NOT":
            self.image2_button['state'] = 'disabled'
        else:
            self.image2_button['state'] = 'normal'

    def perform_operation(self, *args):
        self.update_ui_state()
        
        # Check if we have the necessary images
        if self.image1 is None:
            return
            
        if self.operation.get() == "NOT":
            # For NOT operation, we only need one image
            result = self.operations[self.operation.get()](self.image1)
        else:
            # For other operations, we need both images
            if self.image2 is None:
                return
                
            # Resize images to match
            height = min(self.image1.shape[0], self.image2.shape[0])
            width = min(self.image1.shape[1], self.image2.shape[1])
            img1_resized = cv2.resize(self.image1, (width, height))
            img2_resized = cv2.resize(self.image2, (width, height))
            
            # Perform the operation
            result = self.operations[self.operation.get()](img1_resized, img2_resized)
        
        # Display result
        self.display_image(result, self.result_label, max_size=300)
        self.result = result  # Store for saving
        self.save_button['state'] = 'normal'

    def save_result(self):
        if hasattr(self, 'result'):
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), 
                          ("JPEG files", "*.jpg"),
                          ("All files", "*.*")]
            )
            if file_path:
                cv2.imwrite(file_path, self.result)

def main():
    root = tk.Tk()
    app = BitwiseOperationsUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()