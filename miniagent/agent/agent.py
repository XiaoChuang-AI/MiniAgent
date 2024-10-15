from loguru import logger
from typing import Optional, Dict, List
from miniagent.llm import LLMInput
from miniagent.agent.base import BaseAgent
from miniagent.tools import BaseTool, ToolList
from miniagent.prompt import ReactPromptTemplate, PromptTemplate
from miniagent.agent.utils import extract_action, extract_action_input, split_content, extract_yes_no


class Agent(BaseAgent):
    """
    Agent that interacts with a language model and uses tools to perform actions.
    """

    def __init__(self,
                 llm: Optional[BaseAgent] = None,
                 tools: Optional[ToolList] = None,
                 prompt_template: PromptTemplate = ReactPromptTemplate(),
                 limit: int = 10) -> None:
        """
        Initializes the Agent with a language model, a list of tools, a prompt template, and a step limit.

        Args:
            llm (Optional[BaseAgent]): The language model to be used by the agent.
            tools (Optional[ToolList]): The list of tools the agent can use.
            prompt_template (PromptTemplate): The template for generating prompts.
            limit (int): The maximum number of steps the agent can execute.
        """
        super().__init__()
        self.llm = llm
        self.tools_pocket = {t.tool_name: t for t in tools} if tools else {}
        self.prompt_template = prompt_template
        # self.prompt_kwargs = {x: "" for x in self.prompt_template.input_variables}
        self.prompt_kwargs = {}
        if tools is not None:
            self.prompt_kwargs["tool_names"] = tools.tool_names
            self.prompt_kwargs["tools"] = tools.tool_descriptions
        self.limit = limit

    def _invoke_tool(self, content: str) -> str:
        """
        Invokes a tool based on the action extracted from the content.

        Args:
            content (str): The content from which to extract the action and invoke the corresponding tool.

        Returns:
            str: The original content with the observation (tool output) appended.
        """
        action = extract_action(content)
        if action not in self.tools_pocket:
            logger.error(f"Action '{action}' not found in tools pocket.")
            return content
        action_input, output = extract_action_input(content, [x[0] for x in self.tools_pocket[action].tool_args])
        logger.info("\n" + f"Invoking tool: action={action}, action_input={action_input}")
        try:
            action_output = self.tools_pocket[action].invoke(**action_input)
        except Exception as e:
            logger.error(e)
            action_output = output
        logger.info(f"\nAction output:\n{action_output}")
        return content + f"\nObservation: {action_output}"

    def _step(self, prompt_kwargs: Dict[str, str], print_prompt: bool=True) -> (str, bool):
        """
        Performs a single step of the agent's execution loop.

        Args:
            prompt_kwargs (Dict[str, str]): The variables to be used for formatting the prompt.

        Returns:
            tuple: A tuple containing the response content and a boolean indicating whether the step is final.
        """
        f_prompt = self.prompt_template.format(**prompt_kwargs)
        if print_prompt:
            logger.info("\nPROMPT:\n"+f_prompt+"\n")
        messages = [LLMInput(role="user", content=f_prompt)]
        response = self.llm.invoke(messages=messages)
        logger.info(f"\nLLM output:\n{response.content}")
        use_tool = extract_yes_no(response.content)
        if not use_tool:
            return response.content, True
        action_content = split_content(response.content)
        action_output = self._invoke_tool(content=action_content)
        return action_output, False

    def execute(self, **kwargs) -> Optional[str]:
        """
        Executes the agent's steps, potentially invoking tools and interacting with the language model.

        Args:
        - kwargs: Additional arguments for prompt.
        
        Returns:
            Optional[str]: The final output from the agent after executing the steps, or None if no steps were executed.
        """
        kwargs.update(self.prompt_kwargs)
        prompt_kwargs = {k: kwargs.get(k, None) for k in self.prompt_template.input_variables}
        agent_scratchpad = []  # base input
        for idx in range(self.limit):
            prompt_kwargs["agent_scratchpad"] = "\n".join(agent_scratchpad)
            output, done = self._step(prompt_kwargs, print_prompt=False if idx > 0 else True)
            agent_scratchpad.append(output)
            # logger.info(f"\nSTEP {idx+1}:\n{output}")
            if done:
                break
        if agent_scratchpad:
            agent_output = agent_scratchpad[-1].split("AI:")[-1].strip()
            agent_output = agent_output.replace("`", "")
            return agent_output
