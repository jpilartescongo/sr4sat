# supporting functions for sr implementation

from osgeo import gdal
from PIL import Image
import numpy as np

def convert_to_jpeg(img_path: str, store_path: str):
    """
    Converts a GeoTIFF image to JPEG format with 8-bit RGB.

    Args:
        img_path (str): Path to the input GeoTIFF image.
        store_path (str): Path to save the output JPEG image.
    """
    try:
        gdal_dataset = gdal.Open(img_path)
        if gdal_dataset is None:
            raise ValueError(f"Failed to open GeoTIFF: {img_path}")

        # Read bands
        raster_array = gdal_dataset.ReadAsArray()

        # Handle 3-band RGB (assumes bands are ordered as [bands, height, width])
        if raster_array.ndim == 3 and raster_array.shape[0] >= 3:
            rgb = raster_array[:3, :, :]  # Use only the first 3 bands
            rgb = np.transpose(rgb, (1, 2, 0))  # Convert to HWC

            # Normalize if not uint8
            if rgb.dtype != np.uint8:
                rgb = (255 * (rgb - rgb.min()) / (rgb.max() - rgb.min())).astype(np.uint8)

        elif raster_array.ndim == 2:
            # Single-band grayscale
            rgb = raster_array
            if rgb.dtype != np.uint8:
                rgb = (255 * (rgb - rgb.min()) / (rgb.max() - rgb.min())).astype(np.uint8)
        else:
            raise ValueError("Unsupported number of bands or dimensions.")

        # Save image
        img = Image.fromarray(rgb)
        img.convert("RGB").save(store_path, "JPEG")
        print(f"Image saved to: {store_path}")

    except Exception as e:
        print(f"Error converting GeoTIFF to JPEG: {e}")
