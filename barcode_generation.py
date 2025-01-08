import barcode
from barcode.writer import ImageWriter
import uuid
import os

def generate_barcode(data, folder_path="barcodes"):
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
    barcode_name = f"{data}_{unique_id}"

    # Create the barcode
    barcode_class = barcode.get_barcode_class('code128')
    barcode_instance = barcode_class(data, writer=ImageWriter())

    # Save the barcode image
    file_path = os.path.join(folder_path, barcode_name)
    barcode_instance.save(file_path)

    return barcode_name  # Return the unique barcode name

"""
# Example usage
if __name__ == "__main__":
    data = "12345"  # Replace with the data for the barcode
    unique_barcode = generate_barcode(data)
    print(f"Generated unique barcode: {unique_barcode}")
    
"""