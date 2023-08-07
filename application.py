import aioredis
from fastapi import FastAPI, HTTPException, Request, Response
from PIL import Image
from io import BytesIO
import aiohttp
from mimetypes import guess_type

from strategies import AspectRatioMatchStrategy, ImageProcessor, \
    SimpleResizeStrategy, MaxDimensionResizeStrategy, \
    ThumbnailStrategy, FaceDetectionStrategy, \
    ShrinkAndCenterFaceStrategy

app = FastAPI()

# Connection to Redis
redis = aioredis.from_url("redis://localhost:6379")

async def fetch_image(url: str) -> Image.Image:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail="Image not found")
            image_data = await response.read()
            return Image.open(BytesIO(image_data))
        
@app.get("/{width}/{height}/{image_url:path}")
async def resize_image(request: Request, width: int, height: int, image_url: str, strategy: str = "thumbnail"):

    # Supported resizing strategies
    strategies = {
        "aspect-ratio-match": AspectRatioMatchStrategy(),
        "simple-resize": SimpleResizeStrategy,
        "max-dimension-resize": MaxDimensionResizeStrategy(),
        "thumbnail": ThumbnailStrategy(),
        "face-detection": FaceDetectionStrategy(),
        "shrink-center": ShrinkAndCenterFaceStrategy()
    }

    # Validate the strategy name
    if strategy not in strategies:
        raise HTTPException(status_code=400, detail=f"Invalid strategy name, supported strategies are {list(strategies.keys())}")
    
    # Check the client's "Accept" header for WebP support
    accept_header = request.headers.get("accept", "")
    supports_webp = "image/webp" in accept_header
    content_type = "image/webp" if supports_webp else (guess_type(image_url)[0] or "image/jpeg")
    
    # Construct the cache key
    cache_key = f"{strategy}_{width}x{height}_{image_url}"

    # Check if the image is in cache
    cached_image = await redis.get(cache_key)
    if cached_image:
        return Response(content=cached_image, media_type=content_type)

    # Fetch and resize the image if not cached
    original_image = await fetch_image(image_url)
    # Use WebP format if supported, otherwise use the original format
    output_format = "WEBP" if supports_webp else original_image.format

    # Resize the image
    processor = ImageProcessor(strategies[strategy])
    processed_image = processor.process(original_image, width, height)
    
    # Convert the resized image to bytes
    buffer = BytesIO()
    processed_image.save(buffer, format=output_format)
    processed_image_bytes = buffer.getvalue()
    
    # Store the resized image in the cache
    await redis.set(cache_key, processed_image_bytes)

    return Response(content=processed_image_bytes, media_type=content_type)
        

@app.get("/")
def read_root():
    return {"Hello": "World"}
