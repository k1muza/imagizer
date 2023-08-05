from PIL import Image

from utils.face_detection import FaceCenterDetector


class FaceDetectionStrategy:
    def resize_and_crop(self, original_image: Image.Image, target_width: int, target_height: int):
        # Convert PIL image to OpenCV format (BGR)

        detector = FaceCenterDetector()
        center = detector.detect(original_image)

        # If no faces detected, just resize using AspectRatioStrategy
        if center is None:
            return super().process(original_image, target_width, target_height)

        center_x, center_y = center

        # Determine the cropping box to keep the face in the center
        # Maintain the original aspect ratio while fitting into target dimensions
        target_aspect_ratio = target_width / target_height
        crop_width = min(original_image.width, target_height * target_aspect_ratio)
        crop_height = min(original_image.height, target_width / target_aspect_ratio)

        crop_x1 = max(center_x - crop_width // 2, 0)
        crop_y1 = max(center_y - crop_height // 2, 0)
        crop_x2 = min(center_x + crop_width // 2, original_image.width)
        crop_y2 = min(center_y + crop_height // 2, original_image.height)

        # Crop
        cropped_image = original_image.crop((crop_x1, crop_y1, crop_x2, crop_y2))

        # Resize without distorting
        resized_image = cropped_image.resize((target_width, target_height), Image.LANCZOS)

        return resized_image
