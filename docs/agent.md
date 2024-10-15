- [React Agent](#react-agent)
- [Response Agent](#response-agent)
- [Human Agent](#human-agent)


## React Agent
Agent aims to interact with a language model and use tools to perform actions. It is basically based on the React prompt.

**Use Case**
```python
import httpx
from loguru import logger
from miniagent.llm.gpt import ChatGPT
from miniagent.llm.base import LLMInput
from miniagent.tools import *
from miniagent.agent import Agent

# define the LLM
api_key="sk-xxx"
llm = ChatGPT(api_key=api_key)

# define tools
tools = ToolList([EmailTool(user_email='miniagent.ai@gmail.com', password='xxx', recipient="rayyang0116@gmail.com"),
                    ArxivTool(),])

# define_agent
agent = Agent(llm=llm, tools=tools)

### Search the related topic from arxiv, and send the results of the search to someone.
### you can change the email rayyang0116.gmail.com, r-yang20@tsinghua.org.cn to you own email
user_input = "Please help me search the realted paper about language agent, and send it to rayyang0116.gmail.com, r-yang20@tsinghua.org.cn."
# start!
agent.execute(input=user_input)
```

## Response Agent
ResponseAgent is designed to interact with a language model (LLM) to generate summaries or answers based on tool outputs. The recommended prompt format is:
```python
PromptTemplate(
    prompt="Content: {action_output} your_prompt",
    input_variables=["action_output", "your_variables"]
)
```

**Use Case**
```python
import httpx
from miniagent.agent import ResponseAgent
from miniagent.llm.gpt import ChatGPT
from miniagent.tools import ScrapTool

# define the LLM
api_key="sk-xxx"
llm = ChatGPT(api_key=api_key)
tool = ScrapTool()
scrap_agent = ResponseAgent(
    llm=llm,
    tools=tool,
    prompt=PrompeTemplateV2(prompt="Please summary the content of this website.")
)
output = scrap_agent.execute(url="http://www.maxlikelihood.cn")
print(output)
```
<details>
<summary>Clik to check the output of this example.</summary>

**Likelihood Lab Overview:**

Likelihood Lab is a public AI research initiative founded by Maxwell (Mingwen) Liu and a team of experts from various prestigious institutions, including MIT and Stanford. The lab focuses on advancing technology in FinTech, Energy, and Robotics.

**Research Areas:**
- The lab conducts research in multiple fields, primarily:
  - **FinTech**: Topics include reinforcement learning for market making, asset allocation, stock selection using high-frequency data, and financial sentiment analysis.
  - **Energy and Robotics**: Specific projects in these areas weren't detailed but are part of the lab's scope.

**Highlighted Projects:**
- Reinforcement learning in market making
- Ensemble learning for detecting short-selling
- Machine learning frameworks for stock selection
- Generative adversarial networks for day trading chart generation
- AI applications in games like Mahjong and Gomoku

**Events and Conferences:**
- The lab organizes and participates in various conferences and seminars, focusing on machine learning and quantitative finance, including seasonal research conferences and special events like the Asian Quantitative Finance Conference.

**Team:**
The team includes co-founders and key researchers who bring diverse expertise from notable academic and research institutions.

**Contact Information:**
- Location: Guangzhou, Guangdong, China
- Email: contact@maxlikelihood.cn

The lab aims to leverage AI for societal benefits and innovation across its research areas.

</details>

## Human Agent
HumanAgent serves as an interface for human interaction. It captures input from the user, formats it, and returns it for further processing.

**Use Case**
```python
from miniagent.agent import HumanAgent
human = HumanAgent()
output = human.execute()
```