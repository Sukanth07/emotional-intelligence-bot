from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from src.config import AppConfig

class EmotionalChatbot:
    def __init__(self, chat_history=None):
        """
        Initialize the chatbot with Memory and Groq integration.
        :param chat_history: Existing chat history to load into memory.
        """
        self.memory = ConversationBufferWindowMemory(
            k=AppConfig.MEMORY_WINDOW,
            memory_key="chat_history",
            return_messages=True
        )

        # Load existing chat history into memory if available
        if chat_history:
            for message in chat_history:
                try:
                    self.memory.save_context(
                        {"input": message["human"]},
                        {"output": message["AI"]}
                    )
                except KeyError:
                    print(f"Skipping invalid message: {message}")

        self.default_max_tokens = 100

        # Initialize ChatGroq with default max_tokens
        self.groq_chat = ChatGroq(**AppConfig.LLM_CONFIG, max_tokens=self.default_max_tokens)

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=AppConfig.SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{human_input}")
            ]
        )

        self.conversation = LLMChain(
            llm=self.groq_chat,
            prompt=self.prompt_template,
            memory=self.memory,
            verbose=True
        )

    def adjust_max_tokens(self, user_input):
        """
        Dynamically adjust the max_tokens based on the user's input complexity.
        """
        input_length = len(user_input.split())

        if any(keyword in user_input.lower() for keyword in [
            "explain", "detail", "elaborate", "describe", "clarify", "expand", 
            "analyze", "break down", "in-depth", "why", "how", "discuss", 
            "thorough", "comprehensive", "what do you mean"
        ]) or input_length >= 15:
            return self.default_max_tokens  # More tokens for detailed queries
        else:  # Moderate queries
            return 50  # Balanced token usage

    def generate_response(self, user_input):
        """
        Generate a response using the LLM, with dynamically adjusted max_tokens.
        :param user_input: The user's message.
        :return: The AI's response.
        """
        # Adjust max_tokens dynamically
        max_tokens = self.adjust_max_tokens(user_input)

        # Update the LLM configuration dynamically
        self.groq_chat.max_tokens = max_tokens

        # Generate the response
        return self.conversation.predict(human_input=user_input)
