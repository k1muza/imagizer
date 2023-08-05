from PIL import Image

class ThumbnailStrategy:
    def resize_and_crop(self, image: Image.Image, width: int, height: int) -> Image.Image:
        image.thumbnail((width, height), Image.Resampling.LANCZOS)
        return image
