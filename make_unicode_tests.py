import sys
import re
from codecs import open

if sys.version_info[0] > 2:
    sys.exit(0)

STR_PATTERN = re.compile(r'((?<![\\r])\'(?!__main__).*?(?<!\\)\'|'
                         r'(?<!\\)"(?!__main__).*?(?<!\\)")', re.MULTILINE)

content = open('tests.py', encoding='utf-8').read()
new_content = re.sub(
    STR_PATTERN, lambda m: 'u' + m.group(),
    content.replace('str', 'unicode'),
)

with open('tests_uni.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
