import re


exp = r"\[(.*?)\]"
s_string = "[hello world]"
result = re.findall(exp, s_string)
print(result)