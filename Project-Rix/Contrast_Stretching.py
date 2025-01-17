import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

class ContrastStretchingUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Min-Max Contrast Stretching")
        
        # Variables
        self.processed_image = None
        self.processing = False
        
        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Upload button
        ttk.Button(main_frame, 
                  text="Upload Image", 
                  command=self.upload_image).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Images frame
        images_frame = ttk.Frame(main_frame)
        images_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Processed image
        ttk.Label(images_frame, text="Processed Image").grid(row=0, column=1, padx=10)
        self.processed_label = ttk.Label(images_frame)
        self.processed_label.grid(row=1, column=1, padx=10)
        
        # Debug information display
        self.info_var = tk.StringVar(value="Upload an image to begin")
        ttk.Label(main_frame, 
                 textvariable=self.info_var,
                 wraplength=400).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Save button
        self.save_button = ttk.Button(main_frame, 
                                    text="Save Processed Image", 
                                    command=self.save_image,
                                    state='disabled')
        self.save_button.grid(row=3, column=0, columnspan=2, pady=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff")]
        )
        if file_path:
            # Load image and keep original
            self.original_image = cv2.imread(file_path, 0)  # Read as grayscale
            if self.original_image is None:
                self.info_var.set(f"Error: Could not load image from {file_path}")
                return
            
            # Display debug info
            min_val = np.min(self.original_image)
            max_val = np.max(self.original_image)
            mean_val = np.mean(self.original_image)
            self.info_var.set(f"Original Image Stats:\nMin: {min_val}\nMax: {max_val}\nMean: {mean_val:.2f}")
            
            # Process the image
            self.process_image()

    def display_processed_image(self, image, max_size=400):
        if image is not None:
            # Resize if necessary
            height, width = image.shape
            if height > max_size or width > max_size:
                scale = max_size / max(height, width)
                new_width = int(width * scale)
                new_height = int(height * scale)
                display_image = cv2.resize(image, (new_width, new_height))
            else:
                display_image = image.copy()
            
            # Convert to RGB for display
            display_rgb = cv2.cvtColor(display_image, cv2.COLOR_BGR2RGB)
            
            # Convert to PhotoImage
            image_pil = Image.fromarray(display_rgb)
            photo = ImageTk.PhotoImage(image_pil)
            
            # Update label
            self.processed_label.configure(image=photo)
            self.processed_label.image = photo

    def process_image(self):
        if self.original_image is not None and not self.processing:
            self.processing = True
            
            try:
                # Make a copy for processing
                img_to_process = self.original_image.copy()
                
                # Get min and max values
                min_val = np.min(img_to_process)
                max_val = np.max(img_to_process)
                
                # Check if the image has any contrast
                if min_val == max_val:
                    self.info_var.set("Error: Image has no contrast (min = max)")
                    self.processing = False
                    return
                
                # Perform contrast stretching
                img_float = img_to_process.astype(float)
                minmax_img = np.clip(((img_float - min_val) / (max_val - min_val)) * 255, 0, 255).astype('uint8')
                
                # Update debug info
                new_min = np.min(minmax_img)
                new_max = np.max(minmax_img)
                new_mean = np.mean(minmax_img)
                
                self.info_var.set(
                    f"Processing Complete:\n"
                    f"Original Range: {min_val} to {max_val}\n"
                    f"New Range: {new_min} to {new_max}\n"
                    f"Original Mean: {np.mean(self.original_image):.2f}\n"
                    f"New Mean: {new_mean:.2f}"
                )
                
                # Store and display processed image
                self.processed_image = minmax_img
                self.display_processed_image(minmax_img)
                
                # Enable save button
                self.save_button['state'] = 'normal'
                
            except Exception as e:
                self.info_var.set(f"Error during processing: {str(e)}")
            
            finally:
                self.processing = False

    def save_image(self):
        if self.processed_image is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), 
                          ("JPEG files", "*.jpg"),
                          ("All files", "*.*")]
            )
            if file_path:
                cv2.imwrite(file_path, self.processed_image)
                self.info_var.set("Image saved successfully!")

def main():
    root = tk.Tk()
    app = ContrastStretchingUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()