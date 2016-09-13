# -*- coding: utf-8 -*-

import re
import datetime
import base64

# Because k-prefix is for thousand
THOUSAND_PREFIX = "k"

# Month in russian to their int equivalent
MONTHS = {
    "январ": 1,
    "феврал": 2,
    "март": 3,
    "апрел": 4,
    "ма": 5,
    "июн": 6,
    "июл": 7,
    "август": 8,
    "сентябр": 9,
    "октябр": 10,
    "ноябр": 11,
    "декабр": 12,
}


def extract_id_from_url(article_url):
    """ Extracts id field from URL and encodes it using base64.

    :param article_url: <str>
    :return: <str> (ex. "company/<name>/blog/<id>", "post/<id>/" => base64)
    """

    return base64.b64encode(re.findall(r".ru/(\S+)/", article_url)[0])


def translate_date(note_datetime):
    """ Translates NL datetime to datetime obj

    :param note_datetime: <str> (ex. "сегодня в 10:46" => datetime.now())
    :return:
    """

    print "Encoding note_datetime to utf-8"
    note_datetime = note_datetime.encode("utf-8")

    # Check whether article was created in previous two days
    today_pattern = re.compile("сегодня")
    yesterday_pattern = re.compile("вчера")

    # Patterns for month name, date and time
    time_pattern = re.compile(r"в (\d+):(\d+)")
    date_pattern = re.compile("(\d+) (\S+)")

    if re.findall(today_pattern, note_datetime):
        print "This note was created today"
        datetime_obj = datetime.datetime.now()
    elif re.findall(yesterday_pattern, note_datetime):
        print "This note was created yesterday. Taking away one day from now"
        datetime_obj = datetime.datetime.now() - datetime.timedelta(days=1)
    else:
        print "Manually parsing date of note creation"
        day, month = re.findall(date_pattern, note_datetime)[0]
        print "Day and month found. Extracting month value"
        month = MONTHS[month[:-2]]
        current_year = datetime.date.today().year
        datetime_obj = datetime.datetime(current_year, month, int(day))

    hours, minutes = re.findall(time_pattern, note_datetime)[0]
    datetime_obj.replace(hour=int(hours), minute=int(minutes))
    return str(datetime_obj)


def translate_number(number):
    """ Translates number from str to float. Ex. 2.16k => 2160, 1 111 => 1111

    :param number: <str>
    :return: <float>
    """

    print "Attempting to parse number '{}'".format(number)

    try:
        number = float(number)
        print "Number '{}' parsed without error".format(number)
    except ValueError:
        multiplier = 1
        if "," in number:
            number = number.replace(",", ".")
            print "Character ',' detected. Replaced by '.'"
        if " " in number:
            number = number.replace(" ", "")
            print "Removed whitespace"
        if THOUSAND_PREFIX in number:
            number = number[:-1]
            multiplier = 1000
            print "Thousand prefix detected. Fixed with multiplication"
        number = float(number) * multiplier
    return number
