from pymongo import AsyncMongoClient
from app.core.config import settings

client : AsyncMongoClient | None = None
#initializing client of AsyncMongoClient type as none
db = None

async def connect_to_db():
    global client, db
    client = AsyncMongoClient(settings.MONGODB_URI)
    db = client[settings.DATABASE_NAME]
    
    #try pinging the db
    await client.admin.command("ping")
    await db[settings.PRODUCTS_COLLECTION].create_index("product_identifier")
    print("successfully connected to mongodb")
    


async def disconnect_from_mongodb():
    global client, db
    if client is not None:
        await client.close()
        
        print("Connection closed with mongodb")
        
    
def get_database():
    if db is None:
        raise RuntimeError("Database is not connected yet")
    return db
