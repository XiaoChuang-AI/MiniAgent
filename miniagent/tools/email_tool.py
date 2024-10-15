import re
import yagmail
from miniagent.tools.base import BaseTool
from miniagent.utils.register import TOOL_REGISTER
from typing import List
from loguru import logger


@TOOL_REGISTER
class EmailTool(BaseTool):
    """
    EmailTool is a tool for sending emails. It uses yagmail to send emails to a specified recipient.
    """
    tool_name = "EmailTool"
    tool_description = "This tool is useful when you want to send an email to someone."
    tool_args = [
        ("email", "The email address of the recipient, it's a list"),
        ("subject", "The subject of the email"), 
        ("contents", "The contents of the email"),
        ]

    def __init__(self, user_email: str, password: str, recipient: List) -> None:
        """
        :param user_email: The email address of the sender.
        :param password: The password for the sender's email account.
        :param recipient: The email address of the recipient.
        """
        super().__init__()
        self.user_email = user_email
        self.password = password
        self.recipient = recipient
        
    def _get_email_list(self, input_string: str) -> List:
        # Regular expression pattern for matching email addresses
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'

        # Find all matches of the email pattern in the input string
        email_list = re.findall(email_pattern, input_string)
        return email_list
            
    def invoke(self, email: List | str = [], subject: str = "", contents: str = "") -> None:
        """
        Sends an email with the given subject and contents to the recipient.
        
        :param subject: The subject of the email.
        :param contents: The contents of the email.
        """
        if isinstance(email, str):
            email = self._get_email_list(email)
        email.extend(self.recipient + [self.user_email])
        try:
            with yagmail.SMTP(self.user_email, self.password) as yag:
                yag.send(to=email, subject=subject, contents=contents)
                logger.info(f"Send email to {email}")
            return "The email has been sent. You can execute the next step."
        except Exception as e:
            logger.info(f"An error occurred while sending the email: {e}")

