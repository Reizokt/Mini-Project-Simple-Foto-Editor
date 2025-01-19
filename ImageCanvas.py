import tkinter as tk
from tkinter import Canvas
import cv2
from PIL import Image, ImageTk
import numpy as np
from scipy.signal import wiener
class ImageCanvas(tk.Canvas):
    def __init__(self, master):
        self.width = 600
        self.height = 400
        Canvas.__init__(self, master=master, bg="white", width=self.width, height=self.height)
        self.shown_image = None
        self.transformed_image = None
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
        self.image_blend = None
        self.image_blend_alpha = 0.5
        self.blur_filter = None
        self.edge_detection = None
        self.histogram = False
        self.restoration = []
        self.gamma = 1
        self.image_morph = []
        self.image_match = None
        self.matched_image = None
        self.image_template = None
        self.image_overlay = None
        self.image_overlay_alpha = 1
        self.image_overlay_position = (0,0)
    def show_image(self, img=None):
        self.delete("all")
        image = img
        if img is None:
            print("No image to show")
            return
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width = image.shape[0], image.shape[1]
        if self.resize != (0,0):
            image = cv2.resize(image, (int(width*self.resize[0]), int(height*self.resize[1])))
            height, width = image.shape[0], image.shape[1]

        if self.rotation_degree != 0:
            image = Image.fromarray(image).rotate(self.rotation_degree)
            image = np.array(image)
        if self.translate != (0,0):
            print(image)
            T = np.array([[1,0,self.translate[0]],[0,1,self.translate[1]]],dtype=np.float32)
            image = cv2.warpAffine(image, T, (width, height))
        if self.image_overlay is not None:
            image = self.overlayImage(image)
        if self.image_blend is not None:
            self.image_blend = cv2.cvtColor(self.image_blend, cv2.COLOR_BGR2RGB)
            overlay = cv2.resize(self.image_blend, (width, height))
            blended_b = (1.0 - self.image_blend_alpha) * image[:, :, 0] + self.image_blend_alpha * overlay[:, :, 0]
            blended_g = (1.0 - self.image_blend_alpha) * image[:, :, 1] + self.image_blend_alpha * overlay[:, :, 1]
            blended_r = (1.0 - self.image_blend_alpha) * image[:, :, 2] + self.image_blend_alpha * overlay[:, :, 2]
            image = cv2.merge((blended_b, blended_g, blended_r)).astype(np.uint8)
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
        self.transformed_image = image
        
        if self.isGrayScale:
            image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        if self.color_manipulation != (1,1,1) and len(image.shape) == 3:
            image = np.clip(image * self.color_manipulation, 0, 255).astype(np.uint8)
        if self.contrast_stretch:
            image = self.contrast_stretching(image)
        if self.gamma != 1:
            image = self.gamma_correction(image)
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
        
        if self.edge_detection is not None:
            image = self.applyEdgeFilter(image, self.edge_detection)
        if self.blur_filter is not None:
            image = self.applyBlurFilter(image, self.blur_filter)
        if self.histogram:
            if self.isGrayScale:
                image = cv2.equalizeHist(image)
            else:
                (red, green, blue) = cv2.split(image)
                red = cv2.equalizeHist(red)
                green = cv2.equalizeHist(green)
                blue = cv2.equalizeHist(blue)
                image = cv2.merge([red, green, blue])
        if len(self.restoration) > 0:
            print(self.restoration)
            for restoration in self.restoration:
                image = self.image_restoration(image, restoration)
        if len(self.image_morph) > 0:
            if not self.isGrayScale:
                self.isGrayScale = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            _, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
            for morph in self.image_morph:
                image = self.image_morphing(image, morph)

        if self.image_match is not None:
            image = self.imageMatch(image)
        if self.image_template is not None:
            image = self.templateMatch(image)
        height, width = image.shape[0], image.shape[1]
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
            
    def save(self, path, compression_type):
        image_array = ImageTk.getimage(self.shown_image)
        image_cv2 = np.array(image_array)
        image_cv2 = cv2.resize(image_cv2, (int(image_cv2.shape[1]*self.ratio), int(image_cv2.shape[0]*self.ratio)))
        if self.isGrayScale:
            image_cv2 = cv2.cvtColor(image_cv2, cv2.COLOR_RGB2GRAY)
        else:
            image_cv2 = cv2.cvtColor(image_cv2, cv2.COLOR_RGB2BGR)
        if compression_type == "None":
            cv2.imwrite(path, image_cv2)
        elif compression_type == "DCT":
            image_cv2 = self.compressDCT(image_cv2)
            cv2.imwrite(path, image_cv2)
        elif compression_type == "RLE":
            image_cv2 = self.compressRLE(image_cv2)
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
    def compressDCT(self, image):
        # Function to create a mask through zigzag scanning
        def z_scan_mask(C, N):
            mask = np.zeros((N, N))
            mask_m, mask_n = 0, 0
            for i in range(C):
                if i == 0:
                    mask[mask_m, mask_n] = 1
                else:
                    if (mask_m + mask_n) % 2 == 0:
                        mask_m -= 1
                        mask_n += 1
                        if mask_m < 0:
                            mask_m += 1
                        if mask_n >= N:
                            mask_n -= 1
                    else:
                        mask_m += 1
                        mask_n -= 1
                        if mask_m >= N:
                            mask_m -= 1
                        if mask_n < 0:
                            mask_n += 1
                    mask[mask_m, mask_n] = 1
            return mask

        # Adaptive quantization function
        def adaptive_quantization(coeff, N):
            quant_matrix = np.ones((N, N)) * 10
            quant_matrix[0, 0] = 5  # Keep DC coefficient more accurate
            return np.round(coeff / quant_matrix) * quant_matrix

        # Function to apply compression using DCT and mask generated
        def compress(img, mask, N):
            img_dct = np.zeros_like(img)

            # Process each color channel
            for c in range(img.shape[2]):
                # Iterate through the image in N x N blocks
                for m in range(0, img.shape[0], N):
                    for n in range(0, img.shape[1], N):
                        block = img[m:m+N, n:n+N, c]
                        coeff = cv2.dct(np.float32(block))

                        # Apply the mask (keeping significant coefficients)
                        coeff *= mask

                        # Apply adaptive quantization to preserve details
                        quantized_coeff = adaptive_quantization(coeff, N)

                        # Apply inverse DCT and clip values to avoid overflow
                        iblock = cv2.idct(quantized_coeff)
                        iblock = np.clip(iblock, 0, 255)

                        # Place the compressed block back in the image
                        img_dct[m:m+N, n:n+N, c] = iblock

            return img_dct

        # Set smaller block size (N=8 or N=16) and higher coefficient retention
        N = 8  # Try smaller N (e.g., 8 or 16)
        C = 50  # Keep more coefficients, e.g., 50% of the coefficients

        # Apply compression to the RGB image
        compressed_image = compress(image, z_scan_mask(C, N), N)

        return compressed_image
    def compressRLE(self, image):
        def run_length_encoding(image):
            # Flatten the image
            flattened_image = image.flatten()
            
            # List to store RLE data (value, length)
            rle = []
            
            # Initialize the first value and the count
            prev_val = flattened_image[0]
            count = 1
            
            # Iterate over the flattened image array
            for i in range(1, len(flattened_image)):
                if flattened_image[i] == prev_val:
                    count += 1
                else:
                    rle.append((prev_val, count))
                    prev_val = flattened_image[i]
                    count = 1
            
            # Append the last run
            rle.append((prev_val, count))
            
            return rle

        # Function to apply Run Length Decoding (RLD)
        def run_length_decoding(rle, shape):
            # Create an empty array with the same shape as the original image
            decoded_image = np.zeros(np.prod(shape), dtype=np.uint8)
            
            # Rebuild the image from the RLE data
            idx = 0
            for value, count in rle:
                decoded_image[idx:idx+count] = value
                idx += count
            
            # Reshape the array back to the original shape
            return decoded_image.reshape(shape)
        
        compressed = run_length_encoding(image)
        return run_length_decoding(compressed, image.shape)
    def getTransformedImage(self):
        return cv2.cvtColor(self.transformed_image, cv2.COLOR_RGB2BGR)
    def resetTransformation(self):
        self.transformed_image = None
        self.rotation_degree = 0
        self.translate = (0,0)
        self.resize = (0,0)
        self.image_blend = None
        self.image_blend_alpha = 0.5
        self.image_template = None
        self.image_match = None
        self.matched_image = None
        self.image_overlay = None
        self.image_overlay_alpha = 1
        self.image_overlay_position = (0,0)
    def applyBlurFilter(self, image, blur_filter):
        filtered_image = None
        if blur_filter == "Mean Filter":
            # Mean Filter
            kernel_mean = np.ones((5, 5), np.float32) / 25  # 5x5 mean kernel
            filtered_image = cv2.filter2D(image, -1, kernel_mean)
        elif blur_filter == "Gaussian Filter":
            # Gaussian Filter
            filtered_image = cv2.GaussianBlur(image, (5, 5), sigmaX=1)

        elif blur_filter == "Median Filter":
            # Median Filter
            filtered_image = cv2.medianBlur(image, 5)  # Kernel size 5
        
        else:
            print("Invalid filter type selected.")
            return image
        return filtered_image
    def applyEdgeFilter(self, image, edge_filter):
        if edge_filter == "None":
            return image
        if edge_filter == "Sobel":
            sobel_horizontal = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
            sobel_vertical = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
            sobel_combined = cv2.magnitude(sobel_horizontal, sobel_vertical)
            sobel_filtered = cv2.convertScaleAbs(sobel_combined)
            return sobel_filtered.astype(np.uint8)
        elif edge_filter == "Canny":
            # Apply Canny edge detection
            low_threshold = 50 
            high_threshold = 150
            canny_edges = cv2.Canny(image, low_threshold, high_threshold)
            canny_edges_bgr = cv2.cvtColor(canny_edges, cv2.COLOR_GRAY2BGR)
            return canny_edges_bgr.astype(np.uint8)
        elif edge_filter == "Laplacian":
            laplacian_filtered = cv2.Laplacian(image, cv2.CV_64F)
            laplacian_filtered = cv2.convertScaleAbs(laplacian_filtered)
            return laplacian_filtered.astype(np.uint8)
    def image_restoration(self,image, restoration_type):
        if restoration_type == "Wiener":
            if self.isGrayScale:
                # Convert to float (normalized)
                image_float = image.astype(np.float32) / 255.0
                filtered_image = wiener(image_float, (5, 5))
                
                # Convert back to uint8
                filtered_image = np.clip(filtered_image * 255, 0, 255).astype(np.uint8)
                return filtered_image
            
            # For color images (RGB)
            filtered_image = np.zeros_like(image, dtype=np.float32)
            for i in range(3):  # Apply Wiener filter to each channel
                channel = image[:, :, i].astype(np.float32) / 255.0  # Normalize to [0, 1]
                filtered_image[:, :, i] = wiener(channel, (5, 5))
            
            # Convert back to uint8
            filtered_image = np.clip(filtered_image * 255, 0, 255).astype(np.uint8)
            return filtered_image
        if restoration_type =="Gaussian":
            filtered_image = cv2.GaussianBlur(image, (5, 5), sigmaX=1)
            return filtered_image
        if restoration_type == "Inpainting":
            # Create a mask (with 255 for the area you want to inpaint)
            mask = np.zeros(image.shape[:2], dtype=np.uint8)

            # Define the region to be inpainted (e.g., a square area from (100, 100) to (150, 150))
            mask[100:150, 100:150] = 255  # Marking a region for inpainting

            # Apply inpainting using the selected method
            inpainted = cv2.inpaint(image, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
            return inpainted
    def gamma_correction(self, image):
        image_normalized = image / 255.0
        corrected_image = np.power(image_normalized, self.gamma)
        corrected_image = np.uint8(corrected_image * 255)
        return corrected_image
    def image_morphing(self, image, operation):
        
        kernel_size = 5
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        processed_image = None
        def skeletonize(image):
            if not self.isGrayScale:
                self.isGrayScale = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            # Ensure binary image (0 and 255)
            image = image.copy()
            image[image > 0] = 1
            skeleton = np.zeros(image.shape, np.uint8)
            
            # Get structuring elements for the morphological operations
            kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
            
            while True:
                # Step 1: Erode the image
                eroded = cv2.erode(image, kernel)
                
                # Step 2: Open the eroded image
                opened = cv2.morphologyEx(eroded, cv2.MORPH_OPEN, kernel)
                            
                # Step 3: Subtract to get endpoints
                subset = eroded - opened
                
                # Step 4: Add endpoints to skeleton
                skeleton = cv2.bitwise_or(skeleton, subset)
                
                # Step 5: Erode the original image for next iteration
                image = eroded.copy()
                
                # Step 6: Check if image has been completely eroded
                if cv2.countNonZero(image) == 0:
                    break
            
            # Convert back to binary image with values 0 and 255
            skeleton = skeleton * 255
            return skeleton
        if operation == "Dilation":
            processed_image = cv2.dilate(image, kernel, iterations=1)
        elif operation == "Erosion":
            processed_image = cv2.erode(image, kernel, iterations=1)
        elif operation == "Opening":
            processed_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        elif operation == "Closing":
            processed_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        elif operation == "Boundary Extraction":
            eroded = cv2.erode(image, kernel, iterations=1)
            processed_image = image - eroded
        elif operation == "Skeletonize":
            processed_image = skeletonize(image)
            print(processed_image)
        return processed_image
    def imageMatch(self, image):
        image1 = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        image2 = cv2.cvtColor(self.image_match, cv2.COLOR_BGR2GRAY)
        image2_rgb = cv2.cvtColor(self.image_match, cv2.COLOR_BGR2RGB)
        height1, width1 = image1.shape
        height2, width2 = image2.shape
        if height1 != height2:
            image2 = cv2.resize(image2, (width2, height1))
            image2_rgb = cv2.resize(image2_rgb, (width2, height1))
        sift = cv2.SIFT_create()
        keypoints1, descriptors1 = sift.detectAndCompute(image1, None)
        keypoints2, descriptors2 = sift.detectAndCompute(image2, None)
        image1_with_keypoints = cv2.drawKeypoints(image, keypoints1, None)
        image2_with_keypoints = cv2.drawKeypoints(image2_rgb, keypoints2, None)
        self.matched_image = image2_with_keypoints
        return image1_with_keypoints
    def templateMatch(self, image):
        image_large = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        image_template = cv2.cvtColor(self.image_template, cv2.COLOR_BGR2GRAY)
        cv2.imshow("template", self.image_template)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        result = cv2.matchTemplate(image_large, image_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_loc == (0, 0):
            print("Template found at the top-left corner!")
        else:
            print("Template not found at the top-left corner.")
        top_left = max_loc
        h, w = image_template.shape
        image_matched = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.rectangle(image_matched, top_left, (top_left[0] + w, top_left[1] + h), (0, 255, 0), 3)
        print(f"Top-left: {top_left}, Width: {w}, Height: {h}")
        print(f"Image shape: {image.shape}")
        print(f"Template shape: {image_template.shape}")
        return cv2.cvtColor(image_matched, cv2.COLOR_BGR2RGB)
    
    def overlayImage(self, image):
        # Get the x, y, alpha values and the overlay image
        x, y = self.image_overlay_position
        alpha = self.image_overlay_alpha
        overlay = self.remove_background(self.image_overlay)  # This gives RGBA output

        # Convert the RGB input image to BGR
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Get the size of the image
        height, width = image_bgr.shape[:2]

        # Convert x, y to pixel coordinates
        x = int(x * width)
        y = int(y * height)

        # Get the overlay image size
        overlay_height, overlay_width = overlay.shape[:2]

        # Calculate the region of interest (ROI) in the background image
        overlay_width = min(overlay_width, width - x)
        overlay_height = min(overlay_height, height - y)

        # Ensure the overlay image does not exceed the boundaries of the background
        if overlay_width <= 0 or overlay_height <= 0:
            return image  # No overlay to apply if it's out of bounds

        # Crop the overlay to fit the image dimensions
        overlay_cropped = overlay[:overlay_height, :overlay_width]

        # Extract the channels from the overlay
        overlay_b, overlay_g, overlay_r, overlay_alpha = cv2.split(overlay_cropped)
        overlay_alpha = overlay_alpha / 255.0 * alpha  # Adjust alpha transparency as in your friend's code

        # Get the region of interest (ROI) in the background image
        roi = image_bgr[y:y + overlay_height, x:x + overlay_width]

        # Split the channels of the overlay and the ROI
        background_b, background_g, background_r = cv2.split(roi)

        # Perform alpha blending using the alpha channel
        blended_b = (1.0 - overlay_alpha) * background_b + overlay_alpha * overlay_b
        blended_g = (1.0 - overlay_alpha) * background_g + overlay_alpha * overlay_g
        blended_r = (1.0 - overlay_alpha) * background_r + overlay_alpha * overlay_r

        # Clip the values to be in the valid range (0-255)
        blended_b = np.clip(blended_b, 0, 255).astype(np.uint8)
        blended_g = np.clip(blended_g, 0, 255).astype(np.uint8)
        blended_r = np.clip(blended_r, 0, 255).astype(np.uint8)

        # Merge the channels back together to form the blended ROI
        blended_roi = cv2.merge([blended_b, blended_g, blended_r])

        # Place the blended region back into the original image
        image_bgr[y:y + overlay_height, x:x + overlay_width] = blended_roi

        # Convert the result back to RGB
        result = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

        return result

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