import re
import requests

pattern = re.compile(r"^https://dl\.mehrdl\.top")

with open("download_linnks.txt", "r") as f:
    i = 0
    for line in f:
        url = line.strip()
        if re.match(pattern, url):
            i += 1

    print(i)