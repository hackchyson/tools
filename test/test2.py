# Author: Hack Chyson
# [2018-12-17 19:04:24]


import re

pattern_format = "[# ]*\\[[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\\]"
pattern = re.compile(pattern_format)
print(pattern.match('# [2018-12-17 19:04:24]'))
