from app.models.gemini_model import gemini_model
from app.models.local_model import local_model
from app.core.logger import logger

class EmotionService:

    @staticmethod
    def analyze_emotion(text: str, model_choice: str = "auto"):

        if model_choice in ["gemini", "auto"]:
            try:
                gemini_result = gemini_model.predict(text)
                return gemini_result
            except Exception as gemini_error:
                logger.warning(f"Gemini failed: {gemini_error}")
                if model_choice == "gemini":
                    raise Exception(f"Gemini model failed: {gemini_error}")

        if model_choice in ["local", "auto"]:
            try:
                local_result = local_model.predict(text)
                return local_result
            except Exception as local_error:
                logger.error(f"Local model failed: {local_error}")
                if model_choice == "local":
                    raise Exception(f"Local model failed: {local_error}")
                else:
                    raise Exception("Both Gemini and Local Model failed")
                    
        raise Exception(f"Invalid model choice: {model_choice}")
