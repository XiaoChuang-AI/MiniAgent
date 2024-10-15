import re
import ast
from loguru import logger


def remove_outer_quotes(s):
    # The pattern now correctly handles strings with mismatched quotes at the ends.
    pattern = r'^["\']?(.*?)["\']?$'
    # The non-greedy quantifier `*?` ensures minimal matching inside the quotes.
    s_without_quotes = re.sub(pattern, r'\1', s, flags=re.DOTALL)
    return s_without_quotes

def remove_trailing_newlines_and_special_chars(s):
    # The pattern now correctly handles strings without special characters at the end.
    pattern = r'(\n+[\W_]*)$'
    # The group `(\n+[\W_]*)` captures newlines followed by special characters at the end.
    s_cleaned = re.sub(pattern, '', s)
    return s_cleaned

def processing_string(input_string):
    # Corrected the variable name from `intput_string` to `input_string`.
    funcs = [remove_outer_quotes, remove_trailing_newlines_and_special_chars]
    for func in funcs:
        input_string = func(input_string)  # Apply each function to the input string.
    return input_string.strip()

def extract_action_input(input_string, input_args):
    # Define regex pattern for Action Input
    action_input_pattern = r"Action Input:\s*(?P<action_input>.+)"

    # Search for the Action Input field in the input string
    action_input_match = re.search(action_input_pattern, input_string, re.DOTALL)
    
    # Extract the action input content if a match is found
    action_input_content = action_input_match.group("action_input") if action_input_match else None
    
    # Initialize the dictionary to store extracted arguments
    extracted_args = {}
    output = None
    
    if action_input_content:
        action_input_content = processing_string(action_input_content)
        # Check whether the action_input_content is dict
        try:
            action_input = ast.literal_eval(action_input_content)
            if isinstance(action_input, dict):
                # check whether all expected args are in the input content
                for k, v in action_input.items():
                    if k not in input_args:
                        output = "The Action Input has incorrect input, Please check again." 
                return action_input, output
        except Exception as e:
            logger.warning(f"Action input is not a dict.")
        
        # Iterate over the input arguments and use regex to extract their values
        for i, arg in enumerate(input_args):
            # Look ahead to find the next argument or the end of the string
            next_arg = input_args[i + 1] if i + 1 < len(input_args) else "$"
            # Construct a regex pattern for each argument
            # arg_pattern = rf"{arg}:\s*(?P<{arg}>.+?)(?=\s*{next_arg}:|$)"
            arg_pattern = rf"{arg}\s*[:=]\s*(?P<{arg}>.+?)(?=\s*{next_arg}\s*[:=]\s*|$)"
            arg_match = re.search(arg_pattern, action_input_content, re.DOTALL)
            if arg_match:
                # Add the argument and its extracted value to the dictionary
                extracted_args[arg] = processing_string(arg_match.group(arg).strip())
        # for the input_args, it may not output the key
        if not extracted_args and len(input_args) == 1:
            extracted_args[input_args[0]] = processing_string(action_input_content.strip())
    return extracted_args, output

def extract_action(input_string):
    # Define regex patterns for Action and Action Input
    action_pattern = r"Action:\s*(?P<action>[^\n]+)"

    # Search for matches in the input string
    action_match = re.search(action_pattern, input_string)

    # Extract the action and action input if matches are found
    action = action_match.group("action") if action_match else None

    return action.strip()

def split_content(input_string, split="\nObservation:"):
    return input_string.split("\nObservation:")[0].strip()

def extract_yes_no(input_string):
    # 定义正则表达式模式，匹配 "Thought: Do I need to use a tool?" 后面的 "Yes" 或 "No"
    pattern = r"Thought: Do I need to use a tool\? (Yes|No)"
    
    # 使用正则表达式搜索匹配项
    match = re.search(pattern, input_string)
    
    # 如果找到匹配项，则返回匹配的 "Yes" 或 "No"
    if match:
        flag = match.group(1)  # group(1) 返回第一个括号中匹配的文本
        return True if flag.lower().strip() == "yes" else False
    else:
        return False  # 如果没有找到匹配项，则返回 False
