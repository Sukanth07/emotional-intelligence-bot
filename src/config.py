import os
from dotenv import load_dotenv

load_dotenv()

class AppConfig:
    
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    HF_TOKEN = os.getenv("HF_TOKEN")
    
    # SENTI_API_URL = "https://api-inference.huggingface.co/models/distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    # EMOTION_API_URL = "https://api-inference.huggingface.co/models/bhadresh-savani/distilbert-base-uncased-emotion"

    SYSTEM_PROMPT = (
        "You are a compassionate and emotionally intelligent AI Assistant."
        "Your name is Lumina, and you are an emotionally supportive friend."
        "Your role is to actively listen, understand needs, and respond with kindness, empathy, and positivity."
        "Respond precisely and clearly (max 20 words for concise responses)."
        "For detailed empathetic responses, use no more than 30 words."
    )

    LLM_CONFIG = {
        "model": "llama3-70b-8192",
        "api_key": GROQ_API_KEY,
        "temperature": 0.5,
        "max_retries": 2,
        "streaming": True
    }

    MEMORY_WINDOW = 20