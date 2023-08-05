import cv2
from PIL import Image
import numpy as np


class FaceCenterDetector:
    def detect(self, image: Image.Image):
        # Convert PIL image to OpenCV format (BGR)
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Load a pre-trained face detector
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Detect faces
        faces = face_cascade.detectMultiScale(opencv_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # If no faces detected, return None
        if len(faces) == 0:
            return None

        # Select the first face and calculate center
        face_x, face_y, face_w, face_h = faces[0]
        center_x, center_y = face_x + face_w // 2, face_y + face_h // 2

        return center_x, center_y
