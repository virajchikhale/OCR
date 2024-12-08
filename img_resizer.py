from PIL import Image

def resize_image(input_path, output_path, new_width=None, new_height=None):
    """
    Resize an image with multiple options:
    - Specify exact new width and/or height
    - Specify scale percentage
    
    :param input_path: Path to the input image
    :param output_path: Path to save the resized image
    :param new_width: Desired width (optional)
    :param new_height: Desired height (optional)
    :param scale_percent: Percentage to scale the image (optional)
    """
    # Open the image
    with Image.open(input_path) as img:
        # Get original image dimensions
        original_width, original_height = img.size
        
        # Calculate new dimensions
        # Use specified width and height, or keep original if not specified
        width = new_width if new_width else original_width
        height = new_height if new_height else original_height
        
        # Resize the image
        resized_img = img.resize((width, height), Image.LANCZOS)
        
        # Save the resized image
        resized_img.save(output_path)
        
        print(f"Image resized from {original_width}x{original_height} to {width}x{height}")

# Example usage
def main():
    # Resize by specifying new width and height
    resize_image('test.jpg', 'output_fixed_size.jpg', new_width=2480, new_height=3508)
    
    # Resize by percentage
    # resize_image('input.jpg', 'output_scaled.jpg', scale_percent=50)
    
    # Resize only width, keeping aspect ratio
    # resize_image('input.jpg', 'output_width.jpg', new_width=500)

if __name__ == '__main__':
    main()