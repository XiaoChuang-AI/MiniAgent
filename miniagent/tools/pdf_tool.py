import re
import os
import ftfy
from loguru import logger
from typing import List, Union
from pathlib import Path
from pypdf import PdfReader
from miniagent.tools.base import BaseTool
from miniagent.utils.register import TOOL_REGISTER


@TOOL_REGISTER
class PDFReaderTool(BaseTool):
    tool_name = "PDFReaderTool"
    tool_description = "This tool is useful when you want to read a pdf file."
    tool_args = [
        ("filepath", "A valid path of a pdf file.")
    ]

    def __init__(self, max_length: int = 1024, number_of_pages: Union[str, int] = "all") -> None:
        """
        :param max_length: the max words of parsed file.
        :param number_of_pages: the number of pages to parse. Can be 'all' for all pages or an integer.
        """
        super().__init__()
        self.max_length = max_length
        self.number_of_pages = number_of_pages

    def _invoke(self, filepath: str) -> str:
        """
        Internal method to read and extract text from a PDF file.

        :param file_path: Path to the PDF file.
        :return: Extracted text from the PDF file.
        """
        if Path(filepath).suffix.lower() != ".pdf":
            raise RuntimeError(f"Please input a valid PDF file. Now the input is {filepath}")
        if not os.path.exists(filepath):
            raise RuntimeError("Please input the direct path of a valid PDF file.")
        
        logger.info(f"\nReading a pdf from {filepath}")
        reader = PdfReader(filepath)
        total_pages = len(reader.pages)

        if self.number_of_pages == "all":
            pages_to_read = total_pages
        elif isinstance(self.number_of_pages, int):
            pages_to_read = min(total_pages, self.number_of_pages)
        else:
            raise ValueError("The number_of_pages should be 'all' or an integer.")
        
        output = []
        for page_id in range(pages_to_read):
            text = reader.pages[page_id].extract_text()
            if text:
                output.append(ftfy.fix_text(text))
        return "\n".join(output)
    
    def truncate_string(self, input_string: str) -> str:
        """
        Truncate the input string to a specified number of words.

        :param input_string: The string to be truncated.
        :return: Truncated string.
        """
        words = input_string.split()
        return " ".join(words[:self.max_length])
    
    def invoke(self, filepath: str) -> str:
        """
        Public method to invoke the PDF reading and text extraction.

        :param filepath: Path to the PDF file.
        :return: Extracted and truncated text from the PDF file.
        """
        try:
            output = self._invoke(filepath)
            output = self.truncate_string(output)  # Truncate the text according to a defined length
        except Exception as e:
            logger.info(f"An error occurred: {e}")
            output = str(e)
        return output

if __name__ == "__main__":
    pdftool = PDFReaderTool()
    filepath = "examples/example.pdf"
    output = pdftool.invoke(filepath)
    logger.info(output)
