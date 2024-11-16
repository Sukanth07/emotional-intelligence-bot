class ChatbotException(Exception):
    """Base exception for chatbot-related errors."""
    pass

class LLMLoadingError(ChatbotException):
    """Exception raised for issues while loading the LLM."""
    pass

class ResponseGenerationError(ChatbotException):
    """Exception raised for errors in response generation."""
    pass
