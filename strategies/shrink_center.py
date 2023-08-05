from PIL import Image, ImageOps
from strategies.aspect_ratio_match_strategy import AspectRatioMatchStrategy

from utils.face_detection import FaceCenterDetector


class ShrinkAndCenterFaceStrategy(AspectRatioMatchStrategy):
    def resize_and_crop(self, image: Image.Image, target_width: int, target_height: int):
        # Detect center (e.g., face)
        detector = FaceCenterDetector() # Implement this method for detecting the face
        center_x, center_y = detector.detect(image)

        # If no faces detected, just resize using AspectRatioStrategy
        if center_x is None:
            return super().process(image, target_width, target_height)
        
        # Resize and align
        return self._resize_and_align(image, target_width, target_height, center_x, center_y)
        
    def _resize_and_align(self, image: Image.Image, target_width, target_height, center_x, center_y):
        # Step 1: Shrink down the image until either its width or its height matches with target
        scaling_factor_width = target_width / image.width
        scaling_factor_height = target_height / image.height
        if scaling_factor_width > scaling_factor_height:
            new_width = target_width
            new_height = int(image.height * scaling_factor_width)
            align = "width"
        else:
            new_width = int(image.width * scaling_factor_height)
            new_height = target_height
            align = "height"
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Step 2: Move the face center along the x/y axis in the direction of the center
        if align == "width": # 2a: If widths align first move head along y-axis
            new_center_y = center_y * scaling_factor_width
            top = max(min(new_center_y - target_height // 2, new_height - target_height), 0)
            bottom = top + target_height
            cropped_image = resized_image.crop((0, top, target_width, bottom))
        else: # 2b: If heights align first, move head along x-axis
            new_center_x = center_x * scaling_factor_height
            left = max(min(new_center_x - target_width // 2, new_width - target_width), 0)
            right = left + target_width
            cropped_image = resized_image.crop((left, 0, right, target_height))

        # Step 3: Return the cropped image
        return cropped_image
