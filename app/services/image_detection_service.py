import asyncio
from io import BytesIO

import requests
from PIL import Image

from app.core.config import settings


class ImageDetectionService:
    def __init__(self):
        self.api_url = settings.HUGGINGFACE_DETECTION_URL

    def _get_image_size(self, image_bytes : bytes):
        with Image.open(BytesIO(image_bytes)) as image:
            return image.size

    def _detect_sync(self, image_bytes : bytes, filename : str, content_type : str | None):
        original_width, original_height = self._get_image_size(image_bytes)
        files = {
            "file" : (
                filename or "image",
                image_bytes,
                content_type or "application/octet-stream"
            )
        }

        response = requests.post(
            self.api_url,
            files=files,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        detected_width = data.get("detected_image_width", original_width)
        detected_height = data.get("detected_image_height", original_height)

        return {
            "detections" : data.get("detections", []),
            "original_image" : {
                "width" : original_width,
                "height" : original_height
            },
            "detected_image" : {
                "width" : detected_width,
                "height" : detected_height
            },
            "original_image_width" : original_width,
            "original_image_height" : original_height,
            "detected_image_width" : detected_width,
            "detected_image_height" : detected_height,
            "coordinate_space" : "original_image_pixels"
        }

    async def detect_clothes(self, image_bytes : bytes, filename : str, content_type : str | None):
        return await asyncio.to_thread(
            self._detect_sync,
            image_bytes,
            filename,
            content_type
        )


imageDetectionService = ImageDetectionService()
