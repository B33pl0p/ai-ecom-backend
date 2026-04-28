from fastapi import UploadFile, File
from fastapi import APIRouter
import os
from app.services.feature_extractor import featureVectorExtractor

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
    
    print(image_feature_vectors)
    
    return  {
        "file_name" : file.filename,
        "status" : "File uploaded to temporary directory successfully"
        
    }
    