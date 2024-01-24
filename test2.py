from PIL import Image, ImageDraw
import numpy as np

def validate_badge(image_path):
    # Load the image
    original_image = Image.open(image_path)
    # Validate the size
    if original_image.size != (512, 512):
        raise ValueError("Image size must be 512x512 pixels")

    # Validate non-transparent pixels within a circle
    mask = original_image.convert("L")
    alpha_channel = original_image.split()[3]
    non_transparent_pixels = np.array(alpha_channel) > 0
    non_transparent_pixels_count = np.sum(non_transparent_pixels)
    total_pixels_count = np.prod(original_image.size)

    if non_transparent_pixels_count / total_pixels_count < 0.5:
        raise ValueError("Less than 50% of the badge pixels are non-transparent")

    # Validate happy feeling colors (you can customize this based on your criteria)
    average_color = np.array(original_image).mean(axis=(0, 1))
    if average_color[0] < 100 or average_color[1] < 100 or average_color[2] > 150:
        raise ValueError("The badge does not give a 'happy' feeling")
    
    print("Badge Validated")
    

def convert_badge(image_path):
    # Load the image
    original_image = Image.open(image_path)

    # Convert the image to a circle
    circle_mask = Image.new("L", original_image.size, 0)
    draw = ImageDraw.Draw(circle_mask)
    draw.ellipse((0, 0, 512, 512), fill=255)

    result_image = Image.new("RGBA", original_image.size)
    result_image.paste(original_image, mask=circle_mask)

    return result_image

# Example usage
input_image_path = "sonic.png"
try:
    validated_image = validate_badge(input_image_path)

except ValueError as e:
    print(f"Validation failed: {e}")


converted_image = convert_badge(input_image_path)
converted_image.show()  # Display the result (optional)

# Save the result to a new file
converted_image.save("validated_badge.png")