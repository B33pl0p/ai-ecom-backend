from fastapi import UploadFile, File, Body
from fastapi import APIRouter
import os
from app.core.config import settings
from app.db.database import get_database
from app.services.feature_extractor import featureVectorExtractor
from app.services.pinecone_service import pineconeSearchService

router = APIRouter(prefix="/search")

#create a temporary directory for image upload
TEMP_DIR = "tmp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)


async def get_products_from_search_results(search_results):
    matches = search_results.get("matches", [])
    product_identifiers = [match["id"] for match in matches]
    
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


@router.post("/text")
async def search_by_text(text : str = Body(...)):
    text_feature_vectors = await featureVectorExtractor.extract_text_feature(text)
    search_results = await pineconeSearchService.search_text(text_feature_vectors)
    products = await get_products_from_search_results(search_results)
    
    print(products)
    
    return {
        "text" : text,
        "status" : "Text searched successfully",
        "results" : products
    }
    
