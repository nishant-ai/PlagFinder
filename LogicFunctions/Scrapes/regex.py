import re


import re

s = """https://www.stackoverflow.com/questions/2401628/open-file-in-w-mode-ioerror-errno-2-no-such-file-or-directory """

a = re.findall("www.[a-zA-Z]+.[a-z]+", s)
print(a)