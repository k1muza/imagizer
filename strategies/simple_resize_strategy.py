from PIL import Image

class SimpleResizeStrategy:
    def resize_and_crop(self, image: Image.Image, width: int, height: int) -> Image.Image:
        return image.resize((width, height), Image.Resampling.LANCZOS)
