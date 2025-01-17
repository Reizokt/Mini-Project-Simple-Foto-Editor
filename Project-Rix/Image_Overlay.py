import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

class ImageOverlayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Overlay Controller")
        
        # Initialize image variables
        self.background = None
        self.overlay = None
        self.bg_height = 0
        self.bg_width = 0
        self.ov_height = 0
        self.ov_width = 0
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create image selection buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=0, column=0, columnspan=2, pady=5)
        
        ttk.Button(self.button_frame, text="Select Background Image", 
                  command=self.load_background).grid(row=0, column=0, padx=5)
        ttk.Button(self.button_frame, text="Select Overlay Image", 
                  command=self.load_overlay).grid(row=0, column=1, padx=5)
        
        # Create canvas for image display
        self.canvas = tk.Canvas(self.main_frame, width=800, height=600)
        self.canvas.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Create controls frame
        self.controls_frame = ttk.LabelFrame(self.main_frame, text="Controls", padding="5")
        self.controls_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        # Create sliders (initially disabled)
        self.transparency_var = tk.DoubleVar(value=1.0)
        self.x_pos_var = tk.IntVar(value=0)
        self.y_pos_var = tk.IntVar(value=0)
        
        # Transparency slider
        ttk.Label(self.controls_frame, text="Transparency:").grid(row=0, column=0, sticky=tk.W)
        self.transparency_slider = ttk.Scale(
            self.controls_frame,
            from_=0.0,
            to=1.0,
            orient=tk.HORIZONTAL,
            variable=self.transparency_var,
            command=lambda _: self.update_image(),
            state='disabled'
        )
        self.transparency_slider.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # X position slider
        ttk.Label(self.controls_frame, text="X Position:").grid(row=1, column=0, sticky=tk.W)
        self.x_pos_slider = ttk.Scale(
            self.controls_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.x_pos_var,
            command=lambda _: self.update_image(),
            state='disabled'
        )
        self.x_pos_slider.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Y position slider
        ttk.Label(self.controls_frame, text="Y Position:").grid(row=2, column=0, sticky=tk.W)
        self.y_pos_slider = ttk.Scale(
            self.controls_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.y_pos_var,
            command=lambda _: self.update_image(),
            state='disabled'
        )
        self.y_pos_slider.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Save button (initially disabled)
        self.save_button = ttk.Button(self.main_frame, text="Save Image", 
                                    command=self.save_image, state='disabled')
        self.save_button.grid(row=3, column=0, columnspan=2, pady=5)

    def remove_background(self, image):
        # Create a mask
        mask = np.zeros(image.shape[:2], np.uint8)
        
        # Create temporary arrays for the GrabCut algorithm
        bgdModel = np.zeros((1,65), np.float64)
        fgdModel = np.zeros((1,65), np.float64)
        
        # Create a rectangle around the center of the image
        rect_scale = 0.8  # Scale factor for the rectangle size
        height, width = image.shape[:2]
        margin_x = int(width * (1 - rect_scale) / 2)
        margin_y = int(height * (1 - rect_scale) / 2)
        rect = (margin_x, margin_y, int(width * rect_scale), int(height * rect_scale))
        
        # Apply GrabCut
        cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        
        # Create mask for probable and definite foreground
        mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
        
        # Apply the mask to get the foreground
        foreground = image * mask2[:, :, np.newaxis]
        
        # Create alpha channel
        alpha = mask2 * 255
        
        # Add alpha channel to the foreground
        b, g, r = cv2.split(foreground)
        rgba = cv2.merge([b, g, r, alpha])
        
        return rgba

    def load_background(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")])
        if file_path:
            try:
                self.background = cv2.imread(file_path)
                if self.background is None:
                    raise ValueError("Could not load background image")
                self.bg_height, self.bg_width = self.background.shape[:2]
                self.update_canvas_size()
                self.update_image()
                self.check_enable_controls()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load background image: {str(e)}")
    
    def load_overlay(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")])
        if file_path:
            try:
                # Load image
                original = cv2.imread(file_path)
                if original is None:
                    raise ValueError("Could not load overlay image")
                
                # Remove background
                self.overlay = self.remove_background(original)
                self.ov_height, self.ov_width = self.overlay.shape[:2]
                
                self.update_slider_ranges()
                self.update_image()
                self.check_enable_controls()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load overlay image: {str(e)}")
    
    def update_canvas_size(self):
        # Calculate new canvas size (maintaining aspect ratio)
        max_width = 800
        max_height = 600
        scale = min(max_width/self.bg_width, max_height/self.bg_height)
        self.display_width = int(self.bg_width * scale)
        self.display_height = int(self.bg_height * scale)
        self.canvas.config(width=self.display_width, height=self.display_height)
    
    def update_slider_ranges(self):
        if self.background is not None and self.overlay is not None:
            self.x_pos_slider.configure(to=self.bg_width - self.ov_width)
            self.y_pos_slider.configure(to=self.bg_height - self.ov_height)
    
    def check_enable_controls(self):
        state = 'normal' if (self.background is not None and self.overlay is not None) else 'disabled'
        self.transparency_slider.configure(state=state)
        self.x_pos_slider.configure(state=state)
        self.y_pos_slider.configure(state=state)
        self.save_button.configure(state=state)
    
    def update_image(self):
        if self.background is None or self.overlay is None:
            return
            
        # Create a copy of the background
        result = self.background.copy()
        
        # Get current values
        x = self.x_pos_var.get()
        y = self.y_pos_var.get()
        alpha = self.transparency_var.get()
        
        # Split overlay into channels
        overlay_b, overlay_g, overlay_r, overlay_alpha = cv2.split(self.overlay)
        overlay_alpha = overlay_alpha / 255.0 * alpha
        
        # Define ROI dimensions
        h, w = self.overlay.shape[:2]
        roi_h = min(h, self.bg_height - y)
        roi_w = min(w, self.bg_width - x)
        
        # Adjust overlay dimensions
        overlay_b = overlay_b[:roi_h, :roi_w]
        overlay_g = overlay_g[:roi_h, :roi_w]
        overlay_r = overlay_r[:roi_h, :roi_w]
        overlay_alpha = overlay_alpha[:roi_h, :roi_w]
        
        # Extract ROI from background
        roi = result[y:y + roi_h, x:x + roi_w]
        
        # Alpha blending
        blended_b = (1.0 - overlay_alpha) * roi[:, :, 0] + overlay_alpha * overlay_b
        blended_g = (1.0 - overlay_alpha) * roi[:, :, 1] + overlay_alpha * overlay_g
        blended_r = (1.0 - overlay_alpha) * roi[:, :, 2] + overlay_alpha * overlay_r
        
        # Combine channels
        blended = cv2.merge((blended_b, blended_g, blended_r)).astype(np.uint8)
        
        # Place blended result
        result[y:y + roi_h, x:x + roi_w] = blended
        
        # Convert to PhotoImage for display
        result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        result_small = cv2.resize(result_rgb, (self.display_width, self.display_height))
        self.photo = ImageTk.PhotoImage(Image.fromarray(result_small))
        
        # Update canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
    
    def save_image(self):
        if self.background is None or self.overlay is None:
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), 
                      ("All files", "*.*")]
        )
        
        if file_path:
            # Create final image (same as in update_image)
            result = self.background.copy()
            x = self.x_pos_var.get()
            y = self.y_pos_var.get()
            alpha = self.transparency_var.get()
            
            overlay_b, overlay_g, overlay_r, overlay_alpha = cv2.split(self.overlay)
            overlay_alpha = overlay_alpha / 255.0 * alpha
            
            h, w = self.overlay.shape[:2]
            roi_h = min(h, self.bg_height - y)
            roi_w = min(w, self.bg_width - x)
            
            overlay_b = overlay_b[:roi_h, :roi_w]
            overlay_g = overlay_g[:roi_h, :roi_w]
            overlay_r = overlay_r[:roi_h, :roi_w]
            overlay_alpha = overlay_alpha[:roi_h, :roi_w]
            
            roi = result[y:y + roi_h, x:x + roi_w]
            
            blended_b = (1.0 - overlay_alpha) * roi[:, :, 0] + overlay_alpha * overlay_b
            blended_g = (1.0 - overlay_alpha) * roi[:, :, 1] + overlay_alpha * overlay_g
            blended_r = (1.0 - overlay_alpha) * roi[:, :, 2] + overlay_alpha * overlay_r
            
            blended = cv2.merge((blended_b, blended_g, blended_r)).astype(np.uint8)
            result[y:y + roi_h, x:x + roi_w] = blended
            
            try:
                cv2.imwrite(file_path, result)
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageOverlayApp(root)
    root.mainloop()