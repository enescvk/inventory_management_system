import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont
import uuid
import os

def generate_barcode(name, date, resp_name, exp_date, folder_path="barcodes"):
    """
    Generate a unique barcode and save it as an image.

    Args:
        data (str): The data to encode in the barcode.
        folder_path (str): Directory to save the barcode image. Defaults to 'barcodes'.

    Returns:
        str: The generated barcode's unique identifier.
    """
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Generate a unique ID for the barcode file name
    unique_id = str(uuid.uuid4())
    barcode_name = "temp_barcode"

    # Create the barcode
    barcode_class = barcode.get_barcode_class('code128')
    barcode_instance = barcode_class(unique_id, writer=ImageWriter())
    barcode_instance.writer.text = ""  # Suppress the default text

    # Save the barcode image
    temp_file_path = os.path.join(folder_path, barcode_name)
    barcode_instance.save(temp_file_path)

    # Open the generated barcode
    barcode_image = Image.open(f"{temp_file_path}.png")
    width, height = barcode_image.size

    # Create a new image with extra space for text
    new_height = height + 50  # Add space for text
    new_image = Image.new("RGB", (width, new_height), "white")
    new_image.paste(barcode_image, (0, 0))

    # Add text under the barcode
    draw = ImageDraw.Draw(new_image)

    font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", size=24)  # Adjust the size


    text = f"{name}_{date[:10]}_{resp_name}_{exp_date}"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]  # Width of the text
    text_height = text_bbox[3] - text_bbox[1]  # Height of the text
    text_x = (width - text_width) // 2  # Center text horizontally
    text_y = height + 10  # Add some padding above the text
    draw.multiline_text((text_x, text_y), text, fill="black", font=font, align="center")

    output_file = os.path.join(folder_path, f"{unique_id}.png")
    
    # Save the final image
    new_image.save(output_file)
    
    # Remove temporary barcode file
    os.remove(f"{temp_file_path}.png")

    return unique_id  # Return the unique barcode name

"""
# Example usage
if __name__ == "__main__":
    data = "12345"  # Replace with the data for the barcode
    unique_barcode = generate_barcode(data)
    print(f"Generated unique barcode: {unique_barcode}")
    
"""