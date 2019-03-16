import json

json_config = '/Users/hack/PycharmProjects/tools/memory/review.json'
with open(json_config, "r") as json_file:
    data = json.load(json_file)
