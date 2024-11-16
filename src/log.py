import os
import logging
from src.config import AppConfig


LOGS_DIR = os.path.join(AppConfig.BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# Configure logging
logger = logging.getLogger("EmotionalIntelligenceBot")
logger.setLevel(logging.INFO)

log_file_path = os.path.join(LOGS_DIR, "application.log")

handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
