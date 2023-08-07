# Image Optimization Service

A FastAPI-based service that provides dynamic image resizing and optimization. Users can specify resizing strategies and dimensions through the URL, and the service fetches, processes, and caches the images as needed.

## Features

- Dynamic image resizing with various strategies
- Image centering based on face detection
- Cache integration for faster retrieval of previously processed images
- Supports different image formats

## Resizing Strategies

1. **Aspect Ratio Match**: Matches the aspect ratio of the original image to the target size, `name: "aspect-ratio-match"`.
2. **Simple Resize**: Simple resizing to the target dimensions, `name: "simple-resize"`.
3. **Max Dimension Resize**: Resizes based on the maximum dimension, `name: "max-dimension-resize"`.
4. **Thumbnail Strategy**: Generates a thumbnail of the image, `name: "thumbnail"`.
5. **Face Centering Strategy**: Detects an object of interest (e.g., face) and resizes the image to keep the object in the center, `name: "face-center"`.

## Installation

### Prerequisites

- Python 3.8 or higher
- Redis (for caching)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/image-optimizer.git
   ```

2. Navigate to the project directory:
   ```bash
   cd image-optimizer
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### Usage

You can resize images by accessing URLs in the following format:
```bash
https://your-server.com/<width>/<height>/<image_url>?strategy=<strategy_name>
```

Replace `<width>`, `<height>`, `<image_url>`, and `<strategy_name>` with your desired values.

### License
This project is licensed under the MIT License - see the LICENSE.md file for details.
