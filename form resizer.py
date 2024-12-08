import cv2
import numpy as np

def resize_image(image, max_width=1000):
    """
    Resize image while maintaining aspect ratio
    """
    h, w = image.shape[:2]
    scale = max_width / w
    new_w = int(w * scale)
    new_h = int(h * scale)
    return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

def detect_document_contours(image):
    """
    Advanced document contour detection with multiple strategies
    """
    # Create copies for different processing methods
    original = image.copy()
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Try multiple preprocessing techniques
    preprocessing_methods = [
        # Method 1: Simple thresholding
        cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        
        # Method 2: Adaptive thresholding
        cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                               cv2.THRESH_BINARY, 11, 2),
        
        # Method 3: Canny edge detection
        cv2.Canny(gray, 30, 200)
    ]
    
    # Detection strategies
    all_contours = []
    for preprocessed in preprocessing_methods:
        # Find contours
        contours, _ = cv2.findContours(preprocessed, 
                                       cv2.RETR_EXTERNAL, 
                                       cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter and process contours
        filtered_contours = []
        for cnt in contours:
            # Calculate contour area and perimeter
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            
            # Filter out very small or very large contours
            if area > image.shape[0] * image.shape[1] * 0.1:  # At least 10% of image
                # Approximate polygon
                approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
                
                # Look for quadrilateral (document-like shape)
                if len(approx) == 4:
                    filtered_contours.append(approx)
        
        all_contours.extend(filtered_contours)
    
    # If no contours found, return None
    if not all_contours:
        return None
    
    # Select the largest contour (presumably the document)
    document_contour = max(all_contours, key=cv2.contourArea)
    
    # Reshape contour to 2D array of points
    return document_contour.reshape(-4, 2)

def order_points(pts):
    """
    Order points in top-left, top-right, bottom-right, bottom-left order
    """
    # Compute the center of the rectangle
    center = np.mean(pts, axis=0)
    
    # Sort points relative to center
    sorted_pts = sorted(pts, key=lambda p: np.arctan2(p[1] - center[1], p[0] - center[0]))
    
    return np.array(sorted_pts, dtype="float32")

def four_point_transform(image, pts):
    """
    Apply perspective transform to get top-down view
    """
    # Order points
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # Compute widths and heights
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # Destination points
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # Compute perspective transform
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped

def crop_document(image_path, debug=False):
    """
    Crop document from image with optional debug visualization
    """
    # Read image
    image = cv2.imread(image_path)
    
    # Resize image for processing if too large
    image = resize_image(image)
    
    # Detect document contours
    document_points = detect_document_contours(image)
    
    if document_points is None:
        print("Could not detect document. Returning full image.")
        return image
    
    # Transform perspective
    cropped = four_point_transform(image, document_points)
    
    # Debug visualization
    if debug:
        # Draw contours on original image
        debug_img = image.copy()
        cv2.drawContours(debug_img, [document_points.reshape(-1, 1, 2)], 
                         -1, (0, 255, 0), 3)
        
        # Show images
        cv2.imshow('Original with Contour', debug_img)
        cv2.imshow('Cropped Document', cropped)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return cropped

def main():
    # Example usage
    resize_image('test.jpg', 'output_fixed_size.jpg', new_width=2480, new_height=3508)
    input_image = 'test.jpg'
    
    # Crop document with debug visualization
    cropped = crop_document(input_image, debug=True)
    
    # Optional: Save cropped image
    cv2.imwrite('cropped_document.jpg', cropped)

if __name__ == "__main__":
    main()