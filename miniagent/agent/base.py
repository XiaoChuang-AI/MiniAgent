import logging
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    
    @abstractmethod
    def execute(self):
        # this method will execute the whole process of the Agent
        pass
