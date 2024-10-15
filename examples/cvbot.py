import sys
import httpx
from loguru import logger
from miniagent.llm.gpt import ChatGPT, LLMInput
from miniagent.tools import *
from miniagent.agent import Agent
from miniagent.prompt import ReactPromptTemplate


# define the LLM
api_key = "xxx" # your api key here 
llm = ChatGPT(api_key=api_key, model_name="gpt-3.5-turbo")

# define tools
tools = ToolList([PDFReaderTool(max_length=8000),])

# define_agent
agent = Agent(
    llm=llm, 
    tools=tools,
    prompt_template=ReactPromptTemplate())


user_input = (
    "Please help me analyze the CV in the path './examples/cv.pdf'"
    "summarize the ability and experience of this candidate."
    "propose 10 questions according to its content.")


# start!
output = agent.execute(input=user_input)
# pdftool = PDFReaderTool(max_length=8000)
# output = pdftool.invoke("./examples/cv.pdf")
logger.info("\nFinal output:\n"+output)
