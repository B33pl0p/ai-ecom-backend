from fastapi import APIRouter, Query
from app.core.config import settings
from app.db.database import get_database
from app.schemas.products_schema import ProductsModel

router = APIRouter(prefix="/products", tags = ["Products"])

@router.get("/")
async def get_products(
    page : int = Query(1, ge=1),
    limit : int = Query(10, ge=1, le=100)
):
    db = get_database()
    collection = db[settings.PRODUCTS_COLLECTION]
    skip = (page - 1) * limit
    
    total = await collection.count_documents({})
    documents = await collection.find().skip(skip).limit(limit).to_list(length=limit)
    
    products = []
    
    for doc in documents:
        doc["_id"] = str(doc["_id"])
        products.append(ProductsModel(**doc))
        
    return {
        "page" : page,
        "limit" : limit,
        "total" : total,
        "total_pages" : (total + limit - 1) // limit,
        "products" : products
    }
    
