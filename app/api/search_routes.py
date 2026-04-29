from fastapi import UploadFile, File, Body, HTTPException
from fastapi import APIRouter
import os
from app.core.config import settings
from app.db.database import get_database
from app.services.feature_extractor import featureVectorExtractor
from app.services.image_detection_service import imageDetectionService
from app.services.pinecone_service import pineconeSearchService
from app.services.transliteration_service import transliterationService

router = APIRouter(prefix="/search")

#create a temporary directory for image upload
TEMP_DIR = "tmp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)


async def get_products_from_search_results(search_results):
    matches = search_results.get("matches", [])
    product_identifiers = [match["id"] for match in matches]
    
    if not product_identifiers:
        return []
    
    db = get_database()
    collection = db[settings.PRODUCTS_COLLECTION]
    documents = await collection.find(
        {"product_identifier" : {"$in" : product_identifiers}}
    ).to_list(length=len(product_identifiers))
    
    products_by_identifier = {}
    for doc in documents:
        doc["_id"] = str(doc["_id"])
        products_by_identifier[doc["product_identifier"]] = doc
    
    products = []
    for match in matches:
        product_identifier = match["id"]
        product = products_by_identifier.get(product_identifier)
        
        if product is not None:
            products.append({
                "score" : match.get("score"),
                "product_identifier" : product_identifier,
                "product" : product
            })
    
    return products



@router.post("/image")
async def search_by_image(file : UploadFile = File(...)):
    file_path = os.path.join(TEMP_DIR, file.filename)
    
    with open (file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    #get the feature vectors of the image
    image_feature_vectors = await featureVectorExtractor.extract_image_feature(file_path)
    search_results = await pineconeSearchService.search_image(image_feature_vectors)
    products = await get_products_from_search_results(search_results)
    
    print(products)
    
    return  {
        "file_name" : file.filename,
        "status" : "Image searched successfully",
        "results" : products
        
    }


@router.post("/detect_image")
async def detect_image(file : UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="Image file is empty"
            )

        detection_results = await imageDetectionService.detect_clothes(
            image_bytes,
            file.filename or "image",
            file.content_type
        )
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Image detection failed: {error}"
        )

    return {
        "file_name" : file.filename,
        "status" : "Image detected successfully",
        **detection_results
    }


@router.post("/text")
async def search_by_text(text : str = Body(...)):
    translated_text = await transliterationService.transliterate_to_english(text)
    text_feature_vectors = await featureVectorExtractor.extract_text_feature(translated_text)
    search_results = await pineconeSearchService.search_text(text_feature_vectors)
    products = await get_products_from_search_results(search_results)
    
    print(products)
    
    return {
        "text" : text,
        "translated_text" : translated_text,
        "status" : "Text searched successfully",
        "results" : products
    }
    
