from loguru import logger
from miniagent.agent.base import BaseAgent


class HumanAgent(BaseAgent):
    """
    HumanAgent serves as an interface for human interaction. It captures input from the user,
    formats it, and returns it for further processing.
    """
    
    def __init__(self) -> None:
        """
        Initializes the HumanAgent.
        """
        super().__init__()

    def execute(self) -> str:
        """
        Captures input from the user, formats it, and returns the formatted string.
        
        Returns:
        - str: The formatted user input.
        """
        try:
            content = input("Human input: ")
            formatted_content = f"HUMAN: {content}\n"
            logger.info(f"Captured human input: {formatted_content.strip()}")
            return formatted_content
        except Exception as e:
            logger.error(f"Error capturing human input: {e}")
            raise e
        
if __name__ == "__main__":
    human = HumanAgent()
    output = human.execute()