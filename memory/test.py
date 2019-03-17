import json
import re

json_config = '/Users/hack/PycharmProjects/tools/memory/review.json'
with open(json_config, "r") as json_file:
    data = json.load(json_file)
time_format = data["time_pattern"]
print(time_format)
time_format = re.compile(time_format)

s = "[2019-01-01 Mon]"
print(time_format.match(s))

import datetime
import time

print(time.time())
print(time.asctime())
print(time.struct_time)
print(time.localtime())
print(time.strftime("%Y-%m-%d %a", time.localtime()))
ptime1 = time.strptime("2019-03-17 Sun", "%Y-%m-%d %a")
ptime2 = time.strptime("2019-03-16 Sat", "%Y-%m-%d %a")
ptime3 = time.strptime("2019-03-15 Fri", "%Y-%m-%d %a")

print(ptime1 > ptime2 > ptime3)
print(ptime1 >= ptime1)

print(ptime1)

print(data.get("time_format"))
a = 'hello'
print(a=='hello')

print(len('ooo   '.strip(' ')))