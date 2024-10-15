import arxiv
import ftfy
from loguru import logger
from miniagent.tools.base import BaseTool
from miniagent.utils.register import TOOL_REGISTER
from typing import List


@TOOL_REGISTER
class ArxivTool(BaseTool):
    """
    ArxivTool is a tool for searching academic papers on arXiv.
    
    Attributes:
    - tool_name (str): The name of the tool.
    - tool_description (str): A description of what the tool does.
    - tool_args (List[Tuple[str, str]]): Arguments required by the tool.
    - DOC_CONTENT_CHARS_MAX (int): Maximum number of characters for the document content.
    - top_k_results (int): Number of top results to fetch.
    - sort_criterion (arxiv.SortCriterion): Criterion to sort the search results.
    - sort_order (arxiv.SortOrder): Order to sort the search results.
    - arxiv_kwargs (dict): Additional keyword arguments for the arXiv search.
    """
    
    tool_name = "ArxivTool"
    tool_description = "This tool is useful when you want to search for academic papers on arXiv."
    tool_args = [("query", "The search query, topic or keywords")]
    
    DOC_CONTENT_CHARS_MAX = 40000

    def __init__(self, top_k_results: int = 3, sort_criterion: str = "submittedDate", sort_order: str = "descending", arxiv_kwargs: dict = {}) -> None:
        """
        Initializes the ArxivTool with the given parameters.
        
        Args:
        - top_k_results (int): Number of top results to fetch. Default is 3.
        - sort_criterion (str): Criterion to sort the search results. Default is "submittedDate".
        - sort_order (str): Order to sort the search results. Default is "descending".
        - arxiv_kwargs (dict): Additional keyword arguments for the arXiv search. Default is {}.
        """
        super().__init__()
        self.top_k_results = top_k_results
        
        # Dictionary to map string criteria to arxiv.SortCriterion
        sort_criterion_dict = {
            "relevance": arxiv.SortCriterion.Relevance,
            "lastUpdatedDate": arxiv.SortCriterion.LastUpdatedDate, 
            "submittedDate": arxiv.SortCriterion.SubmittedDate,
        }
        self.sort_criterion = sort_criterion_dict.get(sort_criterion, arxiv.SortCriterion.SubmittedDate)
        
        # Set sort order based on input
        self.sort_order = arxiv.SortOrder.Descending if sort_order == "descending" else arxiv.SortOrder.Ascending
        self.arxiv_kwargs = arxiv_kwargs

    def clean_text(self, text: str) -> str:
        """
        Cleans the input text by fixing encoding issues and removing newlines.
        
        Args:
        - text (str): The text to clean.
        
        Returns:
        - str: The cleaned text.
        """
        return ftfy.fix_text(text.replace('\n', ' '))

    def get_authors(self, authors: List) -> str:
        """
        Converts a list of authors to a comma-separated string.
        
        Args:
        - authors (List): List of authors.
        
        Returns:
        - str: Comma-separated string of authors.
        """
        return ", ".join([str(author) for author in authors])

    def _invoke(self, query: str) -> str:
        """
        Executes the arXiv search with the given query.
        
        Args:
        - query (str): The search query.
        
        Returns:
        - str: Formatted string of search results.
        """
        arxiv_engine = arxiv.Search(
            query=query,
            max_results=self.top_k_results,
            sort_by=self.sort_criterion,
            sort_order=self.sort_order,
            **self.arxiv_kwargs
        )
        output = []
        for result in arxiv_engine.results():
            content = (
                f"Published: {result.published.date()}\n"
                f"URL: {result.entry_id}\n"
                f"Title: {result.title}\n"
                f"Authors: {self.get_authors(result.authors)}\n"
                f"Summary: {self.clean_text(result.summary)}\n"
            )
            output.append(content)
        return "\n".join(output)[:self.DOC_CONTENT_CHARS_MAX]

    def invoke(self, query: str) -> str:
        """
        Public method to invoke the arXiv search with error handling.
        
        Args:
        - query (str): The search query.
        
        Returns:
        - str: Formatted string of search results or error message.
        """
        try:
            output = self._invoke(query)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            output = str(e)
        return output


if __name__ == "__main__":
    arxivtool = ArxivTool(sort_criterion="submittedDate")
    output = arxivtool.invoke("language agent")
    logger.info(output)
    