import os
import re
from bs4 import BeautifulSoup as Soup
from urllib import request
import requests


def download_input_if_not_exists(year):
    day = detect_current_day()
    if day == 0:
        return
    url = f"https://adventofcode.com/{year}/day/{day}/input"

    # Download the file from `url` and save it locally under `file_name`:
    file_name = url.split('/')[-1] + ".txt"

    if os.path.exists(file_name):
        return

    r = request.Request(url)

    session = os.getenv("ADVENTOFCODE_SESSION")

    r.add_header("Cookie", f"session={session}")
    with request.urlopen(r) as response, open(file_name, 'wb') as out_file:
        data = response.read()
        out_file.write(data)

def read_input_lines(filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")
    with open(filename) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]
    return lines

def detect_current_day():
    current_dir = os.getcwd()
    day_pattern = re.compile(r"day(\d+)")
    match = day_pattern.findall(current_dir)
    if len(match) == 0:
        return 0
    return int(match[0])


def post_answer(year, level, answer):
    day = detect_current_day()
    if day == 0:
        return
    url = f"https://adventofcode.com/{year}/day/{day}/answer"

    session = os.getenv("ADVENTOFCODE_SESSION")
    if session is None:
        print("ADVENTOFCODE_SESSION env variable not set !")
        return

    data = {"level": level, "answer": answer}
    cookies = {"session": session}

    response = requests.post(url, data=data, cookies=cookies)

    soup = Soup(response.content, features="html.parser")
    print(soup.find("article").text)


def capture(input_pattern, input_data):
    m = re.compile(input_pattern).match(input_data)
    return m.groups()


def capture_all(input_pattern, input_data):
    m = re.compile(input_pattern).findall(input_data)
    return m
