from typing import Dict, Optional
from abc import ABC, abstractmethod

class BaseTool(ABC):
    """
    BaseTool is an abstract base class for tools. It defines the basic interface
    and common attributes that all tool implementations should have.
    """
    
    @property
    @abstractmethod
    def tool_name(self) -> str:
        """
        The name of the tool. This should be overridden by subclasses.
        """
        pass
    
    @property
    @abstractmethod
    def tool_description(self) -> str:
        """
        The description of the tool. This should be overridden by subclasses.
        """
        pass

    @property
    @abstractmethod
    def tool_args(self) -> str:
        """
        The arguments of the tool. This should be overridden by subclasses.
        """
        pass

    @property
    def format_tool_info(self):
        # Format the arguments as a bulleted list
        arguments = self.tool_args
        if isinstance(arguments, (list, tuple)):
            # Assuming each argument is a tuple of (arg_name, arg_description)
            formatted_args = "\n".join(f"      {arg_name} ({arg_description})" for arg_name, arg_description in arguments)
        else:
            # If arguments is a single string, just use it directly
            formatted_args = arguments

        return (
            f"{self.tool_name}:\n"
            f"    Description:\n"
            f"     {self.tool_description}\n"
            f"    Arguments:\n"
            f"{formatted_args}\n"
        )
    
    def __str__(self) -> str:
        """
        :return: The tool name and its info.
        """
        return self.format_tool_info


class ToolList(list):
    def __init__(self, iterable=None):
        if iterable is not None:
            if not all(isinstance(tool, BaseTool) for tool in iterable):
                raise TypeError("All items must be instances of BaseTool or its subclasses")
            super().__init__(iterable)
        else:
            super().__init__()

    def append(self, tool):
        if not isinstance(tool, BaseTool):
            raise TypeError("Only instances of BaseTool or its subclasses can be added to ToolList")
        super().append(tool)

    def extend(self, iterable):
        if not all(isinstance(tool, BaseTool) for tool in iterable):
            raise TypeError("Only instances of BaseTool or its subclasses can be added to ToolList")
        super().extend(iterable)
    
    @property
    def tool_names(self):
        return ", ".join([tool.tool_name for tool in self])
    
    @property
    def tool_descriptions(self):
        return "\n".join([f"{idx}. {tool.format_tool_info}" for idx, tool in enumerate(self, start=1)])
