from PIL import Image

class MaxDimensionResizeStrategy:
    def resize_and_crop(self, image: Image.Image, width: int, height: int) -> Image.Image:
        original_aspect_ratio = image.width / image.height
        target_aspect_ratio = width / height

        if original_aspect_ratio > target_aspect_ratio:
            new_width = width
            new_height = int(new_width / original_aspect_ratio)
        else:
            new_height = height
            new_width = int(new_height * original_aspect_ratio)

        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
