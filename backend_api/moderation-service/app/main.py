from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline, MarianMTModel, MarianTokenizer
from detoxify import Detoxify
import logging
import torch
from fastapi.exceptions import HTTPException

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device_index = 0 if torch.cuda.is_available() else -1

app = FastAPI(title="Moderation Service")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Глобальні змінні моделей, спочатку None
classifier1 = None
classifier2 = None
translator_tokenizer = None
translator_model = None

@app.on_event("startup")
async def startup_event():
    global classifier1, classifier2, translator_tokenizer, translator_model

    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        device_index = 0 if torch.cuda.is_available() else -1

        classifier1 = pipeline(
            "text-classification",
            model="unitary/toxic-bert",
            device=device_index
        )
        classifier2 = Detoxify('unbiased', device=str(device))

        translator_model_name = "Helsinki-NLP/opus-mt-uk-en"
        translator_tokenizer = MarianTokenizer.from_pretrained(translator_model_name)
        translator_model = MarianMTModel.from_pretrained(translator_model_name)
        translator_model = translator_model.to(device)

        logger.info("Моделі toxic-bert, Detoxify та перекладу успішно ініціалізовані.")

    except Exception as e:
        logger.error(f"Помилка ініціалізації моделей: {str(e)}")
        raise RuntimeError(f"Не вдалося ініціалізувати моделі: {str(e)}")


class TextRequest(BaseModel):
    text: str

@app.post("/moderate")
async def moderate_text(request: TextRequest):
    try:
        if not request.text.strip():
            logger.warning("Отримано порожній текст")
            raise HTTPException(status_code=400, detail="Текст не може бути порожнім")

        if len(request.text) > 512:
            logger.warning(f"Текст занадто довгий: {len(request.text)} символів")
            raise HTTPException(status_code=400, detail="Текст занадто довгий (макс. 512 символів)")

        # Попередня обробка тексту
        processed_text = request.text.strip().lower()
        logger.info(f"Текст після попередньої обробки: {processed_text}")

        # Переклад тексту на англійську для обох моделей
        inputs = translator_tokenizer(processed_text, return_tensors="pt", truncation=True, max_length=512)
        inputs = {k: v.to(device) for k, v in inputs.items()}  # переносимо всі тензори на device
        translated = translator_model.generate(**inputs)
        translated_text = translator_tokenizer.decode(translated[0], skip_special_tokens=True)
        logger.info(f"Перекладений текст: {translated_text}")

        # Обробка тексту моделлю 1 (toxic-bert, перекладений текст)
        result1 = classifier1(translated_text, truncation=True, max_length=512)
        if not result1 or len(result1) == 0:
            raise HTTPException(status_code=500, detail="Порожній результат від моделі toxic-bert")

        label1 = result1[0]["label"].lower()
        score1 = float(result1[0]["score"])
        toxic1 = bool(label1 == "toxic" and score1 > 0.5)

        # Обробка тексту моделлю 2 (Detoxify, перекладений текст)
        result2 = classifier2.predict(translated_text)
        score2_toxicity = float(result2["toxicity"])
        score2_threat = float(result2["threat"])
        score2_insult = float(result2["insult"])
        toxic2 = bool(score2_toxicity > 0.05 or score2_threat > 0.05 or score2_insult > 0.05)

        is_toxic = toxic1 or toxic2
        combined_score = float(max(
            score1 if label1 == "toxic" else (1 - score1),
            score2_toxicity, score2_threat, score2_insult
        ))

        logger.info(
            f"Результат модерації для тексту: {request.text[:50]}..., is_toxic={is_toxic}, score={combined_score:.4f}")
        return {
            "is_toxic": is_toxic,
            "score": combined_score,
            "details": {
                "toxic_bert": {"label": label1, "score": score1},
                "detoxify": {
                    "toxicity": score2_toxicity,
                    "threat": score2_threat,
                    "insult": score2_insult,
                    "translated_text": translated_text
                }
            }
        }

    except Exception as e:
        logger.error(f"Помилка обробки тексту: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))