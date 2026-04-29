# AI Ecommerce Backend

FastAPI backend for an AI-powered ecommerce search experience. It serves paginated products from MongoDB and supports text search, image search, Nepali query normalization, and clothing detection for crop-assisted visual search.

## Features

- Paginated product listing from MongoDB
- CLIP-based text embeddings for semantic product search
- CLIP-based image embeddings for visual product search
- Pinecone vector search for text and image indexes
- Nepali Devanagari and romanized Nepali query normalization through DeepSeek
- Clothing detection proxy for frontend bounding-box and crop workflows
- CORS enabled for frontend integration

## Tech Stack

- Python 3.10+
- FastAPI
- MongoDB
- Pinecone
- OpenAI CLIP
- PyTorch
- DeepSeek API
- Hugging Face hosted detection service

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
tmp_uploads/
README.md
```

## Requirements

The project does not currently include a `requirements.txt`, so install the runtime dependencies manually:

```bash
pip install fastapi uvicorn pydantic-settings pymongo pinecone requests pillow torch python-multipart
pip install git+https://github.com/openai/CLIP.git
```

Depending on your platform, you may want to install PyTorch using the command recommended for your CPU or CUDA setup from the official PyTorch installer.

## Environment Variables

Create a `.env` file in the project root:

```env
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=your_database_name
PRODUCTS_COLLECTION=your_products_collection
PINECONE_API=your_pinecone_api_key
DEEPSEEK_API=your_deepseek_api_key
HUGGINGFACE_DETECTION_URL=https://b33pl0p-clothes-detection-yolov7-deepfashion.hf.space/detect
```

`HUGGINGFACE_DETECTION_URL` is optional because the app defines a default URL in `app/core/config.py`.

## Setup

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

Start the API:

```bash
uvicorn app.main:app --reload
```

The server runs at:

```txt
http://127.0.0.1:8000
```

Interactive API docs are available at:

```txt
http://127.0.0.1:8000/docs
```

## Database Setup

The app connects to MongoDB on startup and creates an index on `product_identifier`.

Product documents should include:

```json
{
  "Name": "Product name",
  "categoryName": "Category",
  "ImageUrl": "https://example.com/image.jpg",
  "masterCategory": "Apparel",
  "product_identifier": "12345"
}
```

`product_identifier` is important because Pinecone match IDs are used to fetch the final product records from MongoDB.

## Pinecone Setup

Create two Pinecone indexes:

```txt
text-index
image-index
```

The backend queries these namespaces:

```txt
text_embedding
image_embedding
```

Each vector ID should match the MongoDB product `product_identifier`.

## API Routes

All routes are mounted under `/api/v1`.

### List Products

```http
GET /api/v1/products/?page=1&limit=10
```

Returns paginated products:

```json
{
  "page": 1,
  "limit": 10,
  "total": 100,
  "total_pages": 10,
  "products": []
}
```

### Text Search

```http
POST /api/v1/search/text
Content-Type: application/json
```

Request body is a raw JSON string:

```json
"rato Nike shoes"
```

The API normalizes the text, creates a CLIP text embedding, searches Pinecone, and returns matching MongoDB products:

```json
{
  "text": "rato Nike shoes",
  "translated_text": "red Nike shoes",
  "status": "Text searched successfully",
  "results": []
}
```

### Image Search

```http
POST /api/v1/search/image
Content-Type: multipart/form-data
```

Form field:

```txt
file
```

The API saves the upload temporarily, creates a CLIP image embedding, searches Pinecone, and returns visually similar products.

### Clothing Detection

```http
POST /api/v1/search/detect_image
Content-Type: multipart/form-data
```

Form field:

```txt
file
```

Example response:

```json
{
  "file_name": "outfit.jpg",
  "status": "Image detected successfully",
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

Frontend flow:

1. Upload an image to `/api/v1/search/detect_image`.
2. Draw the returned bounding boxes over the original image.
3. Let the user choose a detected clothing item.
4. Crop the chosen region in the browser.
5. Send the cropped image to `/api/v1/search/image`.

## Notes

- Uploaded image-search files are written to `tmp_uploads/`.
- Search endpoints currently return the top 5 Pinecone matches.
- DeepSeek transliteration failures fall back to the original query.
- Empty detection uploads return `400`.
- Detection service failures return `502`.
- CORS is currently open to all origins in `app/main.py`; restrict this before production deployment.

## Development Tips

- Use `/docs` to test endpoints through Swagger UI.
- Confirm MongoDB contains products whose `product_identifier` values match Pinecone vector IDs.
- Confirm Pinecone vectors use the same CLIP model and normalization logic as this backend.
- If CLIP or PyTorch installation fails, install PyTorch first using your platform-specific command, then install CLIP.
