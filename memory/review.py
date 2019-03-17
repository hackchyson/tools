import sys
import os
import time
import re
import json

# json configuration file
if len(sys.argv) <= 1:
    json_config = "/Users/hack/PycharmProjects/tools/memory/review.json"
else:
    json_config = sys.argv[1]

with open(json_config, "r") as json_file:
    data = json.load(json_file)

review_paths = data["paths"]  # paths to scan
excludes = data["excludes"]  # if the fullpath contains the elements in the following list, do not scan the content
output_dir = data["output_dir"]
file_format = data["file_format"]
stop_line = data['stop_line']
forgetting = data['forgetting']
time_format = data['time_format']
time_pattern = data['time_pattern']
encoding = data["encoding"]
headline_pattern = data["headline_pattern"]
end = data['end']
# This is for org-mode
# the filename is the first level and the others degrade on level
time_compile = re.compile(time_pattern)
headline_compile = re.compile(headline_pattern)

stop_line_ago = time.time() - stop_line * 24 * 60 * 60  # only scan file's modified time in stop line
output_filename = output_dir + "/" + time.strftime(file_format)

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# to avoid the program runs several times and the result output file have several repeated content
if os.path.exists(output_filename):
    os.remove(output_filename)

# forgetting law
today_str = time.strftime(time_format, time.localtime())
today_zero = time.mktime(time.strptime(today_str, time_format))
oneday = 24 * 60 * 60
periods = [(today_zero - day * oneday, today_zero - (day - 1) * oneday) for day in forgetting]


# to check the time is in the review time or not
def between_time(to_check_time):
    # strptime: string parse time, return structured time, a tuple
    parsed_datetime = time.strptime(to_check_time.strip('\n').strip(' '), time_format)
    sec = time.mktime(parsed_datetime)

    for i in periods:
        if i[0] <= sec <= i[1]:
            return True
    return False


# extract content from file needed to review and write into a review file
def extract(input_filename):
    content_start = False
    input_file = open(input_filename, 'r', encoding=encoding)
    output_file = open(output_filename, 'a', encoding=encoding)
    try:
        for line in input_file:
            match_result = time_compile.match(line.strip('\n'))
            if match_result is not None:
                if between_time(match_result.string) is True:
                    content_start = True
                    output_file.write('* source file: [[' + input_filename + ']]\n')
                    # output_file.write(match_result.string)
                else:
                    content_start = False
            if end == line.strip('\n'):
                content_start = False
            if match_result is None and content_start is True:
                # if the line is headlines, demote one level to make the structure more nice looking
                if headline_compile.match(line) is not None:
                    output_file.write("*" + line)
                else:
                    output_file.write(line)
    except Exception:
        pass


def include():
    flag = True
    for exc in excludes:
        if fullpath.find(exc) != -1:
            return False
    return flag


for path in review_paths:
    for root, dirs, files in os.walk(path):
        for file in files:
            fullpath = root + '/' + file
            mtime = os.path.getmtime(fullpath)
            if mtime < stop_line_ago:  # pass the files that earlier than stop line
                continue
            if include():
                extract(fullpath)

# when the task is done, play a song to remind
# environment: Debian 9
# This are two ways to play out a sound
# 1. paplay
# 2. rhythmbox
# In my test, the paplay command can play my recorded sound,
# but it can not play the mp3 type file download from the internet
# rhythmobx can play all my recorded sound and mp3 files

# os.system("rhythmbox " + music + " 2&>/dev/null &")
# # the song's time
# time.sleep(4 * 60 + 59)
# os.system('rhythmbox-client --quit')
