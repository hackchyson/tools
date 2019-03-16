import sys
import os
import time
import re
import json

# json configuration file
if len(sys.argv) <= 1:
    json_config = "/home/hack/PycharmProjects/tools/memory/review.json"
else:
    json_config = sys.argv[1]

with open(json_config, "r") as json_file:
    data = json.load(json_file)

# paths to scan
review_paths = data["paths"]
# if the fullpath contains the elements in the following list, do not scan the content
excludes = data["excludes"]
output_dir = data["output_dir"]
file_format = data["file_format"]
stop_line = data['stop_line']
forgetting = data['forgetting']

# if the modify time of a file is earlier than one month,
# pass it to reduce the process time
stop_line_ago = time.time() - stop_line * 24 * 60 * 60
output_filename = output_dir + time.strftime(file_format)

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# to avoid the program runs several times and the result output file have several repeated content
if os.path.exists(output_filename):
    os.remove(output_filename)

# forgetting law
now = time.time()
oneday = 24 * 60 * 60
half_day = 12 * 60 * 60
periods = [(now - day * oneday, now - (day - 1) * oneday) for day in forgetting]

# first_point = now - half_day
# second_point = now - oneday
# third_point = now - 2 * oneday
# fourth_point = now - 4 * oneday
# fifth_point = now - 7 * oneday
# sixth_point = now - 15 * oneday
#
# first_period = first_point, now
# second_period = second_point, now
# third_period = third_point, third_point + oneday
# fourth_period = fourth_point, fourth_point + oneday
# fifth_period = fifth_point, fifth_point + oneday
# sixth_period = sixth_point, sixth_point + oneday
#
# periods = first_period, second_period, third_period, fourth_period, fifth_period, sixth_period

# the time format used in my emacs notes is [2018-12-16 21:03:43]
time_pattern_format = "[# ]*\\[[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\\]"
time_pattern = re.compile(time_pattern_format)
headline_pattern_format = "^\\*+ "
headline_pattern = re.compile(headline_pattern_format)


# to check the time is in the review time or not
def between_time(to_check_time):
    # strptime: string parse time, return structured time, a tuple
    parsed_datetime = time.strptime(to_check_time.strip('\n').strip('#').strip(' '), '[%Y-%m-%d %H:%M:%S]')
    sec = time.mktime(parsed_datetime)

    for i in periods:
        if i[0] <= sec <= i[1]:
            return True
    return False


# extract content from file needed to review and write into a review file
def extract(input_filename):
    content_start = False
    input_file = open(input_filename, 'r', encoding='utf8')
    output_file = open(output_filename, 'a', encoding='utf8')
    try:
        for line in input_file:
            match_result = time_pattern.match(line)
            if match_result is not None:
                if between_time(match_result.string) is True:
                    content_start = True
                    output_file.write('* source file: [[' + input_filename + ']]\n')
                    # output_file.write(match_result.string)
                else:
                    content_start = False
            if match_result is None and content_start is True:
                # if the line is headlines, demote one level to make the structure more nice looking
                if headline_pattern.match(line) is not None:
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
            # pass the files that earlier than one month
            if mtime < stop_line_ago:
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
