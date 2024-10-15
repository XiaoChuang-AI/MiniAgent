import openai
import httpx
from typing import Optional, List
from .base import LLMInput, GPTResponse


class ChatGPT:
    """A wrapper class for interacting with OpenAI's GPT models via the chat API."""
    
    def __init__(self, 
                 api_key: Optional[str] = None,
                 base_url: Optional[httpx.URL] = None,
                 http_client: Optional[httpx.Client] = None,
                 model_name: str = "gpt-3.5-turbo",
                 **kwargs) -> None:
        """Initializes the ChatGPT instance with the provided parameters.
        
        Args:
            api_key: The API key for authenticating with the OpenAI API.
            base_url: The base URL for the OpenAI API.
            http_client: An optional httpx.Client instance for making HTTP requests.
            model_name: The name of the model to use for chat completions.
        """
        client = openai.OpenAI(api_key=api_key, base_url=base_url, http_client=http_client, **kwargs)
        self.model = client.chat.completions
        self.model_name = model_name

    def convert_message(self, messages: List[LLMInput]) -> List[dict]:
        """Converts a list of LLMInput objects to the format expected by the OpenAI API.
        
        Args:
            messages: A list of LLMInput objects representing the conversation history.
        
        Returns:
            A list of dictionaries with 'role' and 'content' keys.
        """
        return [{'role': m.role, 'content': m.content} for m in messages]

    def invoke(self, messages: List[LLMInput], temperature: float = 0, **kwargs) -> GPTResponse:
        """Sends messages to the model and returns the model's response.
        
        Args:
            messages: A list of LLMInput objects representing the conversation history.
            temperature: Controls the randomness of the response. Lower values mean less random responses.
        
        Returns:
            A GPTResponse object containing the model's response.
        """
        gpt_messages = self.convert_message(messages)
        output_message = self.model.create(
            model=self.model_name,
            messages=gpt_messages,
            temperature=temperature,
            **kwargs)
        output_message = output_message.choices[0].message
        
        # Assuming output_message is a ChatCompletionMessage object
        return GPTResponse(
            history=messages,
            message=output_message,
            role=output_message.role,
            content=output_message.content.strip())
