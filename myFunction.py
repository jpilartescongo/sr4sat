# supporting functions for sr implementation

from osgeo import gdal
from PIL import Image
import numpy as np
import os

def convert_image_format(input_path: str, output_path: str):
    """
    Converts a geospatial raster image to another format.
    Supports TIFF, JPEG, JPG, PNG as input and output.

    Args:
        input_path (str): Full path to the input image file.
        output_path (str): Full path to save the output image file.

    Returns:
        None
    """
    try:
        # Load the input file using GDAL
        gdal_dataset = gdal.Open(input_path)
        if gdal_dataset is None:
            raise ValueError(f"Failed to open image: {input_path}")

        # Read bands as array (shape: [bands, height, width])
        raster_array = gdal_dataset.ReadAsArray()

        # Handle 3-band RGB
        if raster_array.ndim == 3 and raster_array.shape[0] >= 3:
            rgb = raster_array[:3, :, :]  # Use first 3 bands
            rgb = np.transpose(rgb, (1, 2, 0))  # Convert to HWC
        elif raster_array.ndim == 2:
            rgb = raster_array  # Single-band (grayscale)
        else:
            raise ValueError("Unsupported band configuration.")

        # Normalize if not uint8
        if rgb.dtype != np.uint8:
            rgb = (255 * (rgb - np.min(rgb)) / (np.max(rgb) - np.min(rgb))).astype(np.uint8)

        # Create output directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save to desired format
        Image.fromarray(rgb).convert("RGB").save(output_path)
        print(f"Converted and saved: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
