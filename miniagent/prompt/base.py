from loguru import logger
from abc import ABC, abstractmethod
from typing import Dict, Optional, List, Set
from miniagent.prompt.utils import get_variables_from_str


SYS_PROMPT = "As an advanced and capable AI language model, your role is to "\
            "assist users with their inquiries and tasks comprehensively and without reservation. "\
            "Your objective is to provide accurate information, offer solutions, "\
            "and facilitate task completion to the best of your abilities. Please ensure that "\
            "your responses are informative, helpful, and adhere to the highest standard of assistance."

COT_PROMPT = "Let's think step by step."


class BasePromptTemplate(ABC):
    def prepare_cot(self, x: str):
        return f"{x.strip()}\n{COT_PROMPT}"


class PromptTemplate(BasePromptTemplate):
    """
    PromptTemplate is a template for creating formatted prompts based on given variables.
    
    Attributes:
    - prompt (str): The main prompt template.
    - system_prompt (str): The system-level prompt to prepend to the main prompt.
    - is_cot (bool): Flag indicating if a Chain of Thought (CoT) prompt should be appended.
    - input_variables (List[str]): List of variable names expected in the prompt.

    Examples:
        ```
        prompt = PromptTemplate(
            prompt="Please summarize the content: {content}",
            input_variables=["content"]
        )
        formatted_prompt = prompt.format(content="This is the content.")
        ```
    """
    
    def __init__(self, 
                 prompt: str, 
                 system_prompt: str = SYS_PROMPT, 
                 is_cot: bool = False, 
                 input_variables: List[str] = None) -> None:
        super().__init__()
        self.prompt = f"{system_prompt}\n{prompt}"
        input_variables = input_variables if input_variables is not None else []
        self.input_variables: Set[str] = self.variables | set(input_variables)
        self.is_cot = is_cot

    @property
    def variables(self):
        """
        Extracts variable names from the prompt template.
        
        Returns:
        - Set[str]: A set of variable names found in the prompt template.
        """
        return get_variables_from_str(self.prompt)

    def format(self, **kwargs: Dict[str, str]) -> str:
        """
        Formats the prompt with the given input variables.
        
        Args:
        - **kwargs: Dictionary of variable names and their corresponding values to format the prompt.
        
        Returns:
        - str: The formatted prompt.
        """
        try:
            # Create a dictionary with default empty strings for missing variables
            variable_dict = {k: kwargs.get(k, "") for k in self.input_variables}
            output = self.prompt.format(**variable_dict)
            if self.is_cot:
                output += f"\n{COT_PROMPT}"
            return output
        except KeyError as e:
            logger.error(f"Missing required input variable: {e}")
            raise
        except Exception as e:
            logger.error(f"Error formatting prompt: {e}")
            raise

    def __str__(self) -> str:
        """
        Returns:
        - str: The prompt string.
        """
        return self.prompt