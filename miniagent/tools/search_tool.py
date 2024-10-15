import json
from typing import List
from miniagent.tools.base import BaseTool
from miniagent.utils.register import TOOL_REGISTER
from search_engines import Duckduckgo, Google, Bing
from loguru import logger


@TOOL_REGISTER
class SearchTool(BaseTool):
    """
    SearchTool facilitates internet searches using multiple search engines.
    It is designed to retry searches and parse results into a JSON format.
    """
    tool_name = "SearchTool"
    tool_description = "Useful for searching the internet when unsure about a concept or question."
    tool_args = [("query", "The content to search")]

    def __init__(self, pages: int = 1, top_k: int = 5, retry: int = 5) -> None:
        """
        Initializes the SearchTool with specified settings for pages, top results, and retries.

        :param pages: Number of pages to search through.
        :param top_k: Number of top results to return.
        :param retry: Number of retries if a search fails.
        """
        super().__init__()
        self.search_engine_list = [Duckduckgo(), Google(), Bing()]  # List of search engines
        self.pages = pages
        self.top_k = top_k
        self.retry = retry

    def parse(self, results: List[dict]) -> str:
        """
        Parses the search results and converts them into a JSON formatted string.

        :param results: List of search results. It's a generator.
        :return: JSON string of the top_k results.
        """
        output = [x for x in results]
        output = output[:self.top_k]  # Limit output to top_k
        return json.dumps(output, indent=1)  # Convert to JSON with indentation

    def invoke(self, query: str) -> str:
        """
        Performs the search using the specified query across multiple search engines with retries.

        :param query: The search query.
        :return: JSON formatted string of search results or an error message.
        """
        for engine in self.search_engine_list:
            for attempt in range(self.retry):
                try:
                    results = engine.search(query, pages=self.pages)
                    if results:
                        return self.parse(results)
                except Exception as e:
                    logger.error(f"Error during search with {engine.__class__.__name__}: {e}")
                    if attempt == self.retry - 1:
                        logger.error(f"All retries failed for {engine.__class__.__name__}")
        return "The search result is empty."

# Example usage
if __name__ == "__main__":
    search_tool = SearchTool()
    logger.info(search_tool.invoke("Python programming"))
