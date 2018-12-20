# Author: Hack Chyson
# [2018-12-20 11:27:27]
import json
import time

# print(len('\n'))

json_config = "config.json"
with open(json_config, "r") as json_file:
    data = json.load(json_file)
    print(data["paths"][0])

one_month_ago = time.time() - 30 * 24 * 60 * 60
current_hour = time.gmtime().tm_hour + 8  # beijing time zone
current_day = time.strftime('%Y-%m-%d %H-%M.review')
print(current_day)
