from pinecone import Pinecone

from app.core.config import settings


class PineconeSearchService:
    def __init__(self):
        self.client = Pinecone(api_key=settings.PINECONE_API)

    def format_query_results(self, results):
        if hasattr(results, "to_dict"):
            return results.to_dict()
        
        matches = []
        for match in getattr(results, "matches", []):
            matches.append({
                "id" : getattr(match, "id", None),
                "score" : getattr(match, "score", None),
                "metadata" : getattr(match, "metadata", None)
            })
        
        return {
            "matches" : matches
        }

    async def search_text(self, vector : list[float], top_k : int = 5):
        text_index = self.client.Index("text-index")
        results = text_index.query(
            vector=vector,
            top_k=top_k,
            namespace="text_embedding",
            include_metadata=True
        )
        return self.format_query_results(results)

    async def search_image(self, vector : list[float], top_k : int = 5):
        image_index = self.client.Index("image-index")
        results = image_index.query(
            vector=vector,
            top_k=top_k,
            namespace="image_embedding",
            include_metadata=True
        )
        print("----",results)
        return self.format_query_results(results)


pineconeSearchService = PineconeSearchService()
