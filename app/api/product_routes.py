from fastapi import APIRouter
from app.db.database import get_database
from app.schemas.products_schema import ProductsModel
from typing import List

router = APIRouter(prefix="/products", tags = ["Products"])

@router.get("/", response_model = List[ProductsModel])
async def get_products():
    db = get_database()
    collection = db["products"]
    documents = await collection.find().to_list(length = 10)
    
    products = []
    
    for doc in documents:
        doc["_id"] = str(doc["_id"])
        products.append(ProductsModel(**doc))
        
    return products
    

