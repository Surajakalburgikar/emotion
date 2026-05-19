from transformers import pipeline
from app.core.logger import logger

class LocalEmotionModel:
    def __init__(self):
        try:
            self.classifier = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                top_k=1
            )
            logger.info("Local emotion model loaded successfully")

        except Exception as error:
            logger.error(f"Error loading local model: {error}")
            self.classifier = None

    def predict(self, text: str):
        if not self.classifier:
            raise Exception("Local model not initialized")

        result = self.classifier(text)[0][0]

        return {
            "emotion": result["label"],
            "confidence": round(float(result["score"]), 2),
            "source": "local_model"
        }

local_model = LocalEmotionModel()
