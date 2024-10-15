Now we only support api-based LLM. You can also use ollama to wrap a local LLM as openai-api style.

You can setup a llm by:
```python
from miniagent.llm import ChatGPT, LLMInput

api_key = "xxx"
llm = ChatGPT(api_key)
message = LLMInput(role="user", content="Hey!")
llm.invoke(message)
```
If you want to set `base_url`, `http_client`, and so on. You can input them as kwargs.

