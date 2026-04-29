import torch
import clip
from PIL import Image

class FeatureVectorExtractor:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

    async def extract_image_feature(self, filepath : str):
        
        image = Image.open(filepath).convert("RGB")
        
        image_preprocesed = self.preprocess(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            image_features = self.model.encode_image(image_preprocesed)
        
        image_features= image_features / image_features.norm(dim=-1, keepdim= True)
        return image_features[0].cpu().tolist()     
        
    async def extract_text_feature(self, text : str):
        
        text_tokens = clip.tokenize([text]).to(self.device)
        
        with torch.no_grad():
            text_features = self.model.encode_text(text_tokens)
        
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        return text_features[0].cpu().tolist()
        
    
featureVectorExtractor = FeatureVectorExtractor()
