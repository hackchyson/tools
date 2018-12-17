import time


# review period according to the forgetting law


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

