from pydantic import BaseModel, Field, ConfigDict

class ProductsModel(BaseModel):
    #for alias need to use field
    __id : str | None = None
    Name : str | None = None
    categoryName : str | None = None
    ImageUrl : str | None = None
    masterCategory : str | None = None
    product_identifier : str | None = None
    
    
    
