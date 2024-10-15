from loguru import logger
from typing import List, Set
from miniagent.prompt.base import BasePromptTemplate
from miniagent.prompt.utils import get_variables_from_str


# the base prompt is copied from langchain
REACT_PREFIX_PROMPT = \
"""Assistant is a large language model.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist. 

You can't ask questions back.
"""

REACT_BASE_PROMPT = \
"""Assistant has access to the following tools:
{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action. (you must include the name of of arguments and follow a dict format.
Observation:
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
AI: [your response here]
```
"""

REACT_SUFFIX_PROMPT = \
"""Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}

After you have an observation, you should stop. You can't ask questions back. 
Thought: Do I need to use a tool?"""


class ReactPromptTemplate(BasePromptTemplate):
    """
    To generate prompt templates for a react agent.
    
    Attributes:
    - sys_prompt (str): The combined system-level prompt consisting of prefix and base prompts.
    - suffix_prompt (str): The suffix prompt used as the user content for GPT.
    - prompt (str): The overall prompt combining sys_prompt and suffix_prompt.
    - input_variables (Set[str]): A set of variable names expected in the prompt.

    Examples:
        ```
        prompt_template = ReactPromptTemplate(input_variables=["tools", "tool_names", "chat_history", "input", "agent_scratchpad"])
        formatted_prompt = prompt_template.format(tools="Example tool", tool_names="ExampleTool", chat_history="History", input="New input", agent_scratchpad="Scratchpad")
        ```
    """
    
    def __init__(self,
                 prefix_prompt: str = REACT_PREFIX_PROMPT,
                 base_prompt: str = REACT_BASE_PROMPT,
                 suffix_prompt: str = REACT_SUFFIX_PROMPT,
                 input_variables: List[str] = None) -> None:
        super().__init__()
        self.sys_prompt = "\n".join([prefix_prompt, base_prompt]).strip()  # this can be taken as the system message for the GPT
        self.suffix_prompt = suffix_prompt.strip()  # this is the user content for GPT
        self.prompt = "\n".join([self.sys_prompt, suffix_prompt]).strip()
        input_variables = input_variables if input_variables is not None else []
        self.input_variables: Set[str] = self.variables | set(input_variables)

    @property
    def variables(self) -> Set[str]:
        """
        Extracts variable names from the prompt template.
        
        Returns:
        - Set[str]: A set of variable names found in the prompt template.
        """
        return get_variables_from_str(self.prompt)

    def format(self, **kwargs) -> str:
        """
        Formats the prompt template with the given keyword arguments.
        
        Args:
        - kwargs: Keyword arguments to format the prompt template.
        
        Returns:
        - str: A formatted prompt string.
        """
        try:
            variable_dict = {k: kwargs.get(k, "") for k in self.input_variables}
            output = self.prompt.format(**variable_dict)
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

if __name__=="__main__":
    template = ReactPromptTemplate(input_variables=["tools"])
    logger.info(template)
