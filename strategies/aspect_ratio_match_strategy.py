from PIL import Image


class AspectRatioMatchStrategy:
    def resize_and_crop(self, image: Image.Image, width: int, height: int) -> Image.Image:
        # Calculate the target and original aspect ratios
        target_aspect_ratio = width / height
        original_aspect_ratio = image.width / image.height

        # Calculate the resizing dimensions
        if target_aspect_ratio > original_aspect_ratio:
            new_width = width
            new_height = int(new_width / original_aspect_ratio)
        else:
            new_height = height
            new_width = int(new_height * original_aspect_ratio)

        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Crop the image from the center
        left = (new_width - width) / 2
        top = (new_height - height) / 2
        right = (new_width + width) / 2
        bottom = (new_height + height) / 2
        cropped_image = resized_image.crop((left, top, right, bottom))

        return cropped_image


