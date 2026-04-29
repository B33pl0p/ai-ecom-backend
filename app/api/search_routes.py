from fastapi import UploadFile, File, Body
from fastapi import APIRouter
import os
from app.services.feature_extractor import featureVectorExtractor
from app.services.pinecone_service import pineconeSearchService

router = APIRouter(prefix="/search")

#create a temporary directory for image upload
TEMP_DIR = "tmp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)



@router.post("/image")
async def search_by_image(file : UploadFile = File(...)):
    file_path = os.path.join(TEMP_DIR, file.filename)
    
    with open (file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    #get the feature vectors of the image
    image_feature_vectors = await featureVectorExtractor.extract_image_feature(file_path)
    search_results = await pineconeSearchService.search_image(image_feature_vectors)
    
    print(search_results)
    
    return  {
        "file_name" : file.filename,
        "status" : "Image searched successfully",
        "results" : search_results
        
    }


@router.post("/text")
async def search_by_text(text : str = Body(...)):
    text_feature_vectors = await featureVectorExtractor.extract_text_feature(text)
    search_results = await pineconeSearchService.search_text(text_feature_vectors)
    
    print(search_results)
    
    return {
        "text" : text,
        "status" : "Text searched successfully",
        "results" : search_results
    }
    
