from pinecone import Pinecone

from app.core.config import settings


class PineconeSearchService:
    def __init__(self):
        self.client = Pinecone(api_key=settings.PINECONE_API)

    async def search_text(self, vector : list[float], top_k : int = 5):
        text_index = self.client.Index("text-index")
        results = text_index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True
        )
        return results.to_dict()

    async def search_image(self, vector : list[float], top_k : int = 5):
        image_index = self.client.Index("image-index")
        results = image_index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True
        )
        return results.to_dict()


pineconeSearchService = PineconeSearchService()
