import sys
import os
import time

from memory.each_file import extract

if len(sys.argv) == 1:
    review_path_list = ['/home/hack/notes', '/home/hack/ai', '/home/hack/PycharmProjects/']
else:
    review_path_list = sys.argv[1:]


# if the modify time of a file is earlier than one month,
# pass it to reduce the process time
one_month_ago = time.time() - 30 * 24 * 60 * 60
current_hour = time.gmtime().tm_hour + 8  # beijing time zone
current_day = time.strftime('%Y-%m-%d')
if current_hour <= 11:
    output_filename = '/home/hack/review/' + current_day + '-am.review'
else:
    output_filename = '/home/hack/review/' + current_day + '-pm.review'

exclude_list = ['.git', '.png', '#', '~']

if os.path.exists(output_filename):
    os.remove(output_filename)


def include(fullpath):
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
            if include(fullpath):
                extract(fullpath, output_filename)
