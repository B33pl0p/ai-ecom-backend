import asyncio

import requests

from app.core.config import settings
from app.services.system_prompt import TRANSLITERATION_SYSTEM_PROMPT


class TransliterationService:
    def __init__(self):
        self.api_url = "https://api.deepseek.com/chat/completions"
        self.headers = {
            "Authorization" : f"Bearer {settings.DEEPSEEK_API}",
            "Content-Type" : "application/json"
        }

    def _transliterate_sync(self, query : str):
        payload = {
            "model" : "deepseek-chat",
            "messages" : [
                {
                    "role" : "system",
                    "content" : TRANSLITERATION_SYSTEM_PROMPT
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
        print(response)
        
        data = response.json()
        translated_query = data["choices"][0]["message"]["content"].strip()
        print("====",translated_query)
        return translated_query or query

    async def transliterate_to_english(self, query : str):
        try:
            return await asyncio.to_thread(self._transliterate_sync, query)
        except Exception as error:
            print(f"DeepSeek transliteration failed: {error}")
            return query


transliterationService = TransliterationService()
