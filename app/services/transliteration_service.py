import asyncio

import requests

from app.core.config import settings


class TransliterationService:
    def __init__(self):
        self.api_url = "https://api.deepseek.com/chat/completions"
        self.headers = {
            "Authorization" : f"Bearer {settings.DEEPSEEK_API}",
            "Content-Type" : "application/json"
        }

    def _transliterate_sync(self, query : str):
        payload = {
            "model" : "deepseek-v4-flash",
            "messages" : [
                {
                    "role" : "system",
                    "content" : (
                        "You are a product search query transliteration layer. "
                        "If the user query is in Nepali Devanagari or romanized Nepali, "
                        "convert it into concise English product search words. "
                        "If the query is already English, return the same query cleaned up. "
                        "Return only the final English search phrase. No explanation."
                    )
                },
                {
                    "role" : "user",
                    "content" : query
                }
            ],
            "temperature" : 0,
            "max_tokens" : 40,
            "stream" : False
        }
        
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        translated_query = data["choices"][0]["message"]["content"].strip()
        return translated_query or query

    async def transliterate_to_english(self, query : str):
        try:
            return await asyncio.to_thread(self._transliterate_sync, query)
        except Exception as error:
            print(f"DeepSeek transliteration failed: {error}")
            return query


transliterationService = TransliterationService()
