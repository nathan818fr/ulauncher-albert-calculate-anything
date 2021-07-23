from operator import sub, add
from itertools import zip_longest


def merge_dates(reference_date, dates, signs):
    if not dates:
        return 0, 0, 0, 0, 0, 0

    def extract_date_info(d): return (
        d.year, d.month, d.day, d.hour, d.minute, d.second)

    dates_stats = map(extract_date_info, dates)

    ref_date_info = extract_date_info(reference_date)
    dates_stats = map(lambda d: tuple(map(sub, d, ref_date_info)), dates_stats)

    dates_stats = zip_longest(dates_stats, signs, fillvalue=1)
    dates_stats = map(lambda d: tuple(d[1] * dd for dd in d[0]), dates_stats)

    dates_stats = zip(*dates_stats)
    dates_stats = map(lambda s: add(*s) if len(s) != 1 else s[0], dates_stats)

    years, months, days, hours, minutes, seconds = dates_stats
    return years, months, days, hours, minutes, seconds


def parsedatetime_str(reference_date, dates, signs):
    vals = merge_dates(reference_date, dates, signs)
    info = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']

    vals = zip(vals, info)
    vals = filter(lambda v: v[0], vals)
    vals = map(lambda v: (abs(v[0]), v[1] if v[0] > 0 else v[1] + ' ago'), vals)
    vals = map(lambda v: '{} {}'.format(v[0], v[1]), vals)
    return ', '.join(vals)