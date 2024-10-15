import ftfy
from typing import Optional
from miniagent.tools.base import BaseTool
from miniagent.utils.register import TOOL_REGISTER
from bs4 import BeautifulSoup
from langchain_community.utilities.requests import TextRequestsWrapper
from loguru import logger


DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}


@TOOL_REGISTER
class ScrapTool(BaseTool):
    """
    ScrapTool is designed to extract and return textual content from a given URL.
    """
    tool_name = "ScrapTool"
    tool_description = "Useful when you want to get detailed textual content from an url."
    tool_args = [("url", "The url desired to search.")]

    def __init__(self, text_length: int = 8000):
        super().__init__()
        self.text_length = text_length
        self.requests_wrapper = TextRequestsWrapper(headers=DEFAULT_HEADERS)

    def _invoke(self, url: str = None):
        """
        Internal method to fetch and process the content from the given URL.

        Args:
        - url (str): The URL to scrape.

        Returns:
        - str: Extracted text content, trimmed to the specified length.
        """
        if not url:
            raise ValueError("URL must be provided")
        res = self.requests_wrapper.get(url)
        soup = BeautifulSoup(res, "html.parser") # extract text
        content = ftfy.fix_text(soup.get_text())
        content = content[: self.text_length]
        return content

    def invoke(self, url):
        """
        Public method to invoke the scraping tool with error handling.

        Args:
        - url (str): The URL to scrape.

        Returns:
        - str: Extracted text content or an error message if an exception occurs.
        """
        try:
            output = self._invoke(url=url)
        except Exception as e:
            logger.info(f"An error occurred: {e}")
            output = str(e)
        return output
    

if __name__ == "__main__":
    scraptool = ScrapTool()
    output = scraptool.invoke(url="https://www.langchain.com")
    logger.info(output)
