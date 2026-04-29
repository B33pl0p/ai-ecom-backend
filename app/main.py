from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import db, connect_to_db, disconnect_from_mongodb


from app.api.product_routes import router as product_routes
from app.api.search_routes import router as search_routes
 
#do something on app startup and closeup
@asynccontextmanager 
async def lifespan(app : FastAPI):
    await connect_to_db()
    yield
    await disconnect_from_mongodb()
    

app = FastAPI(title = "AI Ecommerce",
              lifespan= lifespan
              )

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

#just add the router in the main
app.include_router(product_routes, prefix = "/api/v1")
app.include_router(search_routes, prefix="/api/v1")