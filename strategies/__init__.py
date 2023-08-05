from typing import Protocol
from PIL import Image

from .aspect_ratio_match_strategy import AspectRatioMatchStrategy
from .simple_resize_strategy import SimpleResizeStrategy
from .max_dimension_resize_strategy import MaxDimensionResizeStrategy
from .thumbnail_strategy import ThumbnailStrategy
from .face_detection_strategy import FaceDetectionStrategy
from .shrink_center import ShrinkAndCenterFaceStrategy


class ResizingStrategy(Protocol):
    def resize_and_crop(self, image: Image.Image, width: int, height: int) -> Image.Image:
        pass


class ImageProcessor:
    def __init__(self, strategy: ResizingStrategy) -> None:
        self.strategy = strategy

    def process(self, image: Image.Image, width: int, height: int) -> Image.Image:
        return self.strategy.resize_and_crop(image, width, height)
