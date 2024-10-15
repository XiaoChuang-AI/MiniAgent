import os
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
tools = ToolList([
    EmailTool(
        user_email='xxx', # repalce to your email
        password='xxx', # replace to your passward
        recipient=["miniagent.ai@gmail.com"]),
    ArxivTool(top_k_results=10),])

# define_agent
agent = Agent(
    llm=llm, 
    tools=tools,
    prompt_template=ReactPromptTemplate())

user_input = "Please help me search the realted paper about language agent, and send all of them to rayyang0116.gmail.com, r-yang20@tsinghua.org.cn."
# start!
agent.execute(input=user_input)
