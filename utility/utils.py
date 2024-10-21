import re
import json

def fix_json(json_str):
    # Escape unescaped backslashes (i.e., backslashes that are not part of an existing escape sequence)
    json_str = re.sub(r'(?<!\\)\\(?![\\"])', r"\\\\", json_str)

    # Remove trailing commas in JSON arrays and objects
    json_str = re.sub(r',\s*([\]}])', r'\1', json_str)

    return json_str

def fix_json_content(content):
    # Fix improperly formatted strings, handling cases where single quotes should be preserved
    content = re.sub(r'(\w)"(\w)', r'\1\'\2', content)  # Fix "word"s" to "word's"
    
    # Replace stray single quotes with double quotes in keys/values
    content = re.sub(r'(?<=[:,\s])\'(?=\w+\'?\s*[:,\]])', '"', content)  # Replace single quotes in keys/values

    # Replace \\n with actual newlines (\n)
    content = content.replace("\\n", "\n")
    
    return content


def fix_quotes(content):
    # Ensure all quotes are correctly formatted around JSON keys/values
    content = re.sub(r'(?<=[:,\s])\'(?=\w+\'?\s*[:,\]])', '"', content)
    return content