from osgeo import gdal
from PIL import Image

def convert_to_jpeg(img_path: str, store_path: str):
    """
    Converts a GeoTIFF image to JPEG format.

    Args:
        img_path (str): Path to the input GeoTIFF image.
        store_path (str): Path to store the output JPEG image.

    Returns:
        None
    """
    try:
        # Open the GeoTIFF file
        gdal_dataset = gdal.Open(img_path)
        if gdal_dataset is None:
            raise ValueError(f"Failed to open GeoTIFF file: {img_path}")

        # Read the raster data as an array
        raster_array = gdal_dataset.ReadAsArray()

        # If the raster array has multiple bands, combine them into an RGB image
        if len(raster_array.shape) == 3:
            # Convert to RGB format assuming 3 bands (R, G, B)
            img = Image.fromarray(raster_array.transpose(1, 2, 0))
        else:
            # Convert single-band (grayscale) to an image
            img = Image.fromarray(raster_array)

        # Save the image as JPEG
        img.convert("RGB").save(store_path, "JPEG")
        print(f"Image successfully converted and saved at: {store_path}")

    except Exception as e:
        print(f"Error during conversion: {e}")
