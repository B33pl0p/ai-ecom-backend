# AI Ecommerce Backend

FastAPI backend for an AI-powered ecommerce search system. The API supports product pagination, text search, image search, Nepali query normalization, and clothes detection through a HuggingFace-hosted YOLOv7 model.

## Features

- Paginated product listing from MongoDB
- Text search using CLIP text embeddings and Pinecone
- Image search using CLIP image embeddings and Pinecone
- Nepali Devanagari and romanized Nepali query normalization through DeepSeek
- Clothes detection proxy for bounding box detection
- Detection-assisted image search support for frontend cropping workflows

## Project Structure

```txt
app/
  api/
    product_routes.py
    search_routes.py
  core/
    config.py
  db/
    database.py
  schemas/
    products_schema.py
  services/
    feature_extractor.py
    image_detection_service.py
    pinecone_service.py
    system_prompt.py
    transliteration_service.py
  main.py
FRONTEND_API_DOCUMENTATION.md
README.md
```

## Requirements

- Python 3.10+
- MongoDB database
- Pinecone account and indexes
- DeepSeek API key
- HuggingFace Space for clothes detection

Main Python packages used by the project:

```txt
fastapi
uvicorn
pydantic-settings
pymongo
pinecone
requests
pillow
torch
git+https://github.com/openai/CLIP.git
python-multipart
```

## Environment Variables

Create a `.env` file in the project root.

```env
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=your_database_name
PRODUCTS_COLLECTION=your_products_collection
PINECONE_API=your_pinecone_api_key
DEEPSEEK_API=your_deepseek_api_key
HUGGINGFACE_DETECTION_URL=https://b33pl0p-clothes-detection-yolov7-deepfashion.hf.space/detect
```

`HUGGINGFACE_DETECTION_URL` is optional because the backend already has a default value.

## Pinecone Setup

The backend expects two Pinecone indexes:

```txt
text-index
image-index
```

The backend uses these namespaces:

```txt
text_embedding
image_embedding
```

Each vector id should match the product `product_identifier` stored in MongoDB. Search results are matched back to MongoDB products using that identifier.

## MongoDB Product Shape

Products should include these fields:

```json
{
  "Name": "Product name",
  "categoryName": "Category",
  "ImageUrl": "https://example.com/image.jpg",
  "masterCategory": "Apparel",
  "product_identifier": "12345"
}
```

The backend creates an index on `product_identifier` during startup.

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install fastapi uvicorn pydantic-settings pymongo pinecone requests pillow torch python-multipart
pip install git+https://github.com/openai/CLIP.git
```

## Running The Server

Start the FastAPI app:

```bash
uvicorn app.main:app --reload
```

Default local URL:

```txt
http://127.0.0.1:8000
```

Interactive API docs:

```txt
http://127.0.0.1:8000/docs
```

## API Overview

All routes are mounted under:

```txt
/api/v1
```

### Products

```http
GET /api/v1/products/?page=1&limit=10
```

Returns paginated products from MongoDB.

### Text Search

```http
POST /api/v1/search/text
Content-Type: application/json
```

Request body is a raw JSON string:

```json
"rato Nike shoes"
```

The backend normalizes Nepali or romanized Nepali queries before creating the text embedding.

### Image Search

```http
POST /api/v1/search/image
Content-Type: multipart/form-data
```

Form field:

```txt
file
```

Returns visually similar products from the image Pinecone index.

### Clothes Detection

```http
POST /api/v1/search/detect_image
Content-Type: multipart/form-data
```

Form field:

```txt
file
```

Returns bounding boxes and image dimensions:

```json
{
  "detections": [
    {
      "bbox": [120, 80, 420, 560],
      "confidence": 0.91,
      "class": 0
    }
  ],
  "original_image": {
    "width": 800,
    "height": 1000
  },
  "detected_image": {
    "width": 800,
    "height": 1000
  },
  "coordinate_space": "original_image_pixels"
}
```

The frontend can draw these boxes over the uploaded image, let the user select one, crop that selected region in the browser, and send the cropped image to `/api/v1/search/image`.

## Frontend Integration

See [FRONTEND_API_DOCUMENTATION.md](./FRONTEND_API_DOCUMENTATION.md) for detailed frontend request and response examples, pagination behavior, bounding box scaling, and detection-assisted search flow.

## Notes

- Uploaded image search files are temporarily written to `tmp_uploads`.
- DeepSeek transliteration failures fall back to the original query.
- Detection failures return a `502` response from the backend route.
- Empty detection uploads return a `400` response.
