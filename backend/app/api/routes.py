from fastapi import APIRouter
from app.schemas.emotion_schema import EmotionRequest
from app.services.emotion_service import EmotionService
from app.utils.response_helper import success_response, error_response

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@router.post("/analyze")
def analyze_emotion(payload: EmotionRequest):

    try:
        text = payload.text.strip()

        if not text:
            return error_response("Input text cannot be empty", 400)

        result = EmotionService.analyze_emotion(text, payload.model)

        return success_response(result)

    except Exception as error:
        return error_response(str(error), 500)
