from pinecone import Pinecone

from app.core.config import settings


class PineconeSearchService:
    def __init__(self):
        self.client = Pinecone(api_key=settings.PINECONE_API)
        self.text_index = self.client.Index("text-index")
        self.image_index = self.client.Index("image-index")

    async def search_text(self, vector : list[float], top_k : int = 5):
        results = self.text_index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True
        )
        return results.to_dict()

    async def search_image(self, vector : list[float], top_k : int = 5):
        results = self.image_index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True
        )
        return results.to_dict()


pineconeSearchService = PineconeSearchService()
