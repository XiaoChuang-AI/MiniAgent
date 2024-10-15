from typing import List, Optional
from dataclasses import dataclass, field
from openai.types.chat import ChatCompletionMessage


@dataclass
class LLMInput:
    role: str = "user"
    content: str = ""

    def __post_init__(self):
        valid_roles = {"user", "assistant", "system"}
        if self.role not in valid_roles:
            raise ValueError(f"Invalid role: {self.role}. Valid roles are: {valid_roles}")


@dataclass
class GPTResponse:
    history: List[LLMInput] = field(default_factory=list)
    message: Optional[ChatCompletionMessage] = None
    role: str = "assistant"
    content: str = ""

