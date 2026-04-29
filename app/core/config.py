from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGODB_URI : str
    DATABASE_NAME : str
    PRODUCTS_COLLECTION : str
    PINECONE_API : str
    DEEPSEEK_API : str
    HUGGINGFACE_DETECTION_URL : str = "https://b33pl0p-clothes-detection-yolov7-deepfashion.hf.space/detect"
    
    #infer the values using the environment file
    model_config = SettingsConfigDict(env_file = ".env", extra = "ignore")
    
settings = Settings()

    
