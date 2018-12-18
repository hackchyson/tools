import sys
import os
import time
import re

# the directories to scan to extract content to review
if len(sys.argv) == 1:
    review_path_list = ['/home/hack/notes', '/home/hack/ai', '/home/hack/PycharmProjects/']
else:
    review_path_list = sys.argv[1:]

# if the modify time of a file is earlier than one month,
# pass it to reduce the process time
one_month_ago = time.time() - 30 * 24 * 60 * 60

current_hour = time.gmtime().tm_hour + 8  # beijing time zone
current_day = time.strftime('%Y-%m-%d')

# output_filename
if current_hour <= 11:
    output_filename = '/home/hack/review/' + current_day + '-am.review'
else:
    output_filename = '/home/hack/review/' + current_day + '-pm.review'

# if the fullpath contains the elements in the following list, do not scan the content
exclude_list = ['.git', '.png', '#', '~']

# to avoid the program runs several times and the result output file have several repeated content
if os.path.exists(output_filename):
    os.remove(output_filename)

# forgetting law
now = time.time()
one_day = 24 * 60 * 60
half_day = 12 * 60 * 60

first_point = now - half_day
second_point = now - one_day
third_point = now - 2 * one_day
fourth_point = now - 4 * one_day
fifth_point = now - 7 * one_day
sixth_point = now - 15 * one_day

first_period = first_point, now
second_period = second_point, now
third_period = third_point, third_point + one_day
fourth_period = fourth_point, fourth_point + one_day
fifth_period = fifth_point, fifth_point + one_day
sixth_period = sixth_point, sixth_point + one_day

periods = first_period, second_period, third_period, fourth_period, fifth_period, sixth_period

# the time format used in my emacs notes is [2018-12-16 21:03:43]
pattern_format = "[# ]*\\[[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\\]"
pattern = re.compile(pattern_format)


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
            match_result = pattern.match(line)
            if match_result is not None:
                if between_time(match_result.string) is True:
                    content_start = True
                    output_file.write('* source file: [[' + input_filename + ']]\n')
                    output_file.write(match_result.string)
                else:
                    content_start = False
            if match_result is None and content_start is True:
                output_file.write(line)
    except Exception:
        pass


def include():
    flag = True
    for exc in exclude_list:
        if fullpath.find(exc) != -1:
            return False
    return flag


for path in review_path_list:
    for root, dirs, files in os.walk(path):
        for file in files:
            fullpath = root + '/' + file
            mtime = os.path.getmtime(fullpath)
            # pass the files that earlier than one month
            if mtime < one_month_ago:
                continue
            if include():
                extract(fullpath)
