from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.database import db, connect_to_db, disconnect_from_mongodb


from app.api.product_routes import router as product_routes
 
#do something on app startup and closeup
@asynccontextmanager 
async def lifespan(app : FastAPI):
    await connect_to_db()
    yield
    await disconnect_from_mongodb()
    

app = FastAPI(title = "AI Ecommerce",
              lifespan= lifespan
              )

#just add the router in the main
app.include_router(product_routes, prefix = "/api/v1")