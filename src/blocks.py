import re

def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")
    split_lines = []
    for line in lines:
        line = line.strip()
        if line != "":
            split_lines.append(line.strip())
    return split_lines

def is_heading(text):
    regex = r"^#{1,6} .*$"
    return re.search(regex, text) != None

def is_code(text):
    regex = r"^```(.|\n)+```$"
    return re.search(regex, text) != None

def is_quote_block(text):
    regex = r"^(>.*\n)*(>.*)$"
    return re.search(regex, text) != None

def is_unordered_list(text):
    regex = r"^((\+|-) .*\n)*(\+|-) .*$"
    return re.search(regex, text) != None

def is_ordered_list(text):
    lines = text.split("\n")
    for i in range(0, len(lines)):
        regex = f"^{i + 1}. .*$"
        line_result = re.search(regex, lines[i])
        if line_result == None:
            return False
    return True

def block_to_block_type(input_block):
    if is_heading(input_block):
        return "heading"
    if is_code(input_block):
        return "code"
    if is_quote_block(input_block):
        return "quote"
    if is_unordered_list(input_block):
        return "unordered list"
    if is_ordered_list(input_block):
        return "ordered list"
    return "paragraph"