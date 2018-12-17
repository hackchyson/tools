import re
import time
from memory.forgetting import periods

# the time format used in my emacs notes is [2018-12-16 21:03:43]
pattern_format = "[# ]*\\[[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\\]"
pattern = re.compile(pattern_format)


def between_time(to_check_time):
    # strptime: string parse time, return structured time, a tuple
    parsed_datetime = time.strptime(to_check_time.strip('\n').strip('#').strip(' '), '[%Y-%m-%d %H:%M:%S]')
    sec = time.mktime(parsed_datetime)

    for i in periods:
        if i[0] <= sec <= i[1]:
            return True
    return False


def extract(input_filename, output_filename):
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


def test():
    extract('/home/hack/test/input_test', '/home/hack/test/output_test')
