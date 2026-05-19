import google.generativeai as genai
from app.core.config import settings
from app.core.logger import logger

# Models tried in order — fastest/cheapest first
GEMINI_MODEL_CASCADE = [
    "gemini-2.5-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash-lite-001",
    "gemini-2.0-flash-001",
    "gemini-2.0-flash",
    "gemma-4-31b-it",
    "gemma-4-26b-a4b-it",
]


class GeminiEmotionModel:
    def __init__(self):
        try:
            if not settings.GEMINI_API_KEY:
                raise ValueError("Missing Gemini API key")
            genai.configure(api_key=settings.GEMINI_API_KEY)
            logger.info("Gemini client configured successfully")
            self.available = True
        except Exception as error:
            logger.error(f"Gemini initialization failed: {error}")
            self.available = False

    def _build_prompt(self, text: str) -> str:
        return f"""Detect the primary emotion from the following text.

Return ONLY one word — no punctuation, no explanation — chosen from:
happy, sad, angry, fear, surprise, disgust, neutral

Text: {text}
"""

    def predict(self, text: str) -> dict:
        if not self.available:
            raise Exception("Gemini client not configured (missing API key)")

        last_error = None
        for model_name in GEMINI_MODEL_CASCADE:
            try:
                logger.info(f"Trying Gemini model: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(self._build_prompt(text))
                emotion = response.text.strip().lower().split()[0]  # take first word only
                # Format model name beautifully, e.g. gemini-2.5-flash -> Gemini 2.5 Flash
                display_name = model_name.replace("-it", "").replace("-", " ").title()
                logger.info(f"Success with model: {model_name}, emotion: {emotion}")
                return {
                    "emotion": emotion,
                    "confidence": 0.95,
                    "source": display_name
                }
            except Exception as error:
                err_str = str(error)
                if "429" in err_str or "quota" in err_str.lower():
                    logger.warning(f"{model_name} quota exceeded, trying next model...")
                    last_error = f"Quota exceeded on {model_name}"
                elif "404" in err_str or "not found" in err_str.lower():
                    logger.warning(f"{model_name} not found, trying next model...")
                    last_error = f"Model not found: {model_name}"
                else:
                    logger.error(f"{model_name} failed with: {error}")
                    last_error = str(error)
                    break  # Non-quota error — stop trying

        raise Exception(
            f"All Gemini models exhausted their quota or failed. Last error: {last_error}. "
            f"The local model will be used as fallback."
        )


gemini_model = GeminiEmotionModel()
