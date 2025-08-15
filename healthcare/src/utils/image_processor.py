from PIL import Image
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def optimize_image(image_bytes, max_width=800):
    """
    Optimize the image by resizing while maintaining aspect ratio and original format.
    Returns bytes of the optimized image.
    """
    try:
        # Open image from bytes
        image = Image.open(io.BytesIO(image_bytes))
        original_format = image.format or 'JPEG'
        
        # Calculate new dimensions maintaining aspect ratio
        width, height = image.size
        if width > max_width:
            ratio = max_width / width
            new_size = (max_width, int(height * ratio))
            image = image.resize(new_size, Image.LANCZOS)
            logger.info(f"Resized image from {width}x{height} to {new_size[0]}x{new_size[1]}")
        
        # Save image to bytes in original format
        output = io.BytesIO()
        image.save(output, format=original_format, optimize=True)
        output.seek(0)
        
        optimized_size = len(output.getvalue()) / 1024  # Size in KB
        logger.info(f"Optimized image size: {optimized_size:.2f}KB (Format: {original_format})")
        
        return output.getvalue()
        
    except Exception as e:
        logger.error(f"Error optimizing image: {str(e)}")
        return image_bytes

def preprocess_image(file):
    """
    Process the uploaded file (image or PDF).
    Returns bytes of the file content.
    """
    if file is None:
        logger.error("No file provided")
        return None
        
    try:
        # For both images and PDFs, just return the file bytes
        return file.getvalue()
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return None