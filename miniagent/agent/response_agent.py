from loguru import logger
from typing import Optional, Dict, List, Union
from miniagent.llm import LLMInput
from miniagent.agent.base import BaseAgent
from miniagent.tools import BaseTool, ToolList
from miniagent.prompt import PromptTemplate


class ResponseAgent(BaseAgent):
    """
    ResponseAgent is designed to interact with a language model (LLM) to generate 
    summaries or answers based on tool outputs. The recommended prompt format is:
    
    PromptTemplateV2(
        prompt="Content: {action_output} your_prompt",
        input_variables=["action_output", "your_variables"]
    )
    """
    
    def __init__(self,
                 llm: Optional[BaseAgent] = None,
                 tools: Optional[Union[ToolList, BaseTool]] = None,
                 prompt: Optional[PromptTemplate] = None) -> None:
        """
        Initializes the ResponseAgent.
        
        Parameters:
        - llm (Optional[BaseAgent]): The language model to use.
        - tools (Optional[Union[ToolList, BaseTool]]): The tools for generating action outputs.
        - prompt (Optional[PrompeTemplateV2]): The prompt template to use.
        """
        super().__init__()
        self.llm = llm
        self.tool = tools[0] if isinstance(tools, ToolList) else tools

        if prompt is None:
            raise ValueError("Prompt cannot be None")

        if "action_output" not in prompt.input_variables:
            prompt = PromptTemplate(
                prompt="Content: {action_output} " + prompt.prompt,
                input_variables=prompt.input_variables + ["action_output"]
            )
        self.prompt = prompt

    def _invoke_tool(self, **kwargs) -> str:
        """
        Invokes the tool and retrieves the action output.
        
        Parameters:
        - kwargs: Additional arguments for the tool.
        
        Returns:
        - str: The output from the tool.
        """
        action_input = {k: kwargs.get(k, None) for (k, _) in self.tool.tool_args}
        action = self.tool.tool_name
        logger.info(f"Invoking tool: action={action}, action_input={action_input}")
        
        try:
            action_output = self.tool.invoke(**action_input)
        except Exception as e:
            logger.error(f"Error invoking tool: {e}")
            raise e
        
        return action_output

    def execute(self, **kwargs) -> str:
        """
        Executes the agent by invoking the tool and generating a response from the LLM.
        
        Args:
        - kwargs: Additional arguments for the tool and prompt.
        
        Returns:
        - str: The response from the LLM.
        """
        action_output = self._invoke_tool(**kwargs)
        
        f_prompt = self.prompt.format(action_output=action_output, **kwargs)
        logger.info(f"\nPROMPT:\n{f_prompt}\n")
        
        messages = [LLMInput(role="user", content=f_prompt)]
        
        try:
            response = self.llm.invoke(messages=messages)
            response = response.content
        except Exception as e:
            logger.error(f"Error invoking LLM: {e}")
            raise e
        
        return response
    

if __name__ == "__main__":
    import httpx
    from miniagent.llm.gpt import ChatGPT
    from miniagent.tools import ScrapTool
    
    # define the LLM
    base_url="https://api.xty.app/v1"
    api_key="sk-9jM8OjXj2fhwHG2FC4F4Bd6e40F4425585E7BcCbBb3e28Ed"
    http_client=httpx.Client(
        base_url="https://api.xty.app/v1",
        follow_redirects=True,
    )
    llm = ChatGPT(
        base_url=base_url,
        api_key=api_key,
        http_client=http_client,
    )
    tool = ScrapTool()
    scrap_agent = ResponseAgent(
        llm=llm,
        tools=tool,
        prompt=PromptTemplate(prompt="Please summary the content of this website.")
    )
    output = scrap_agent.execute(url="http://www.maxlikelihood.cn")
    print(output)