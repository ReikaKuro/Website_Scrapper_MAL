import json
import requests
import urllib3.exceptions
from bs4 import BeautifulSoup
import re
import time

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

count = 1
fail = 0
dictionary = {}
start_time_program = time.time()


def get_and_parse(site_id):
    req = requests.get(f"https://myanimelist.net/anime/{site_id}", headers, timeout=5)
    print('Getting info took %s seconds' % (time.time() - start_time))
    bs = BeautifulSoup(req.content, 'html.parser')
    parsed_title = str(bs.title)
    print('Parsing took %s seconds' % (time.time() - start_time))
    return parsed_title


def regex(parsed_title):
    regexed_title = re.sub('<[a-zA-Z]*>|</[a-zA-Z]*>|(?: - MyAnimeList.net)|[\n]', '', parsed_title)
    print('Regex took %s seconds' % (time.time() - start_time))
    print(str(count) + ' : ' + str(regexed_title))
    return regexed_title

while True:
    start_time = time.time()

    try:
        title = get_and_parse(count)
        final_title_format = regex(title)
        if final_title_format != '404 Not Found':
            dictionary[final_title_format] = count
            print('Adding to Dictionary took %s seconds' % (time.time() - start_time))
        # print(bs.prettify())

    except TimeoutError or urllib3.exceptions.ConnectTimeoutError or urllib3.connectionpool.HTTPSConnectionPool as e:
        print(str(count) + ' : ' + str(e))
        error_count = 0

        while error_count < 5:
            try:
                title = get_and_parse(count)
                final_title_format = regex(title)
                if title != '404 Not Found':
                    dictionary[final_title_format] = count

            except Exception as e:
                error_count += 1
                pass
        pass

    except Exception as e:
        print(str(count) + ' : ' + str(e))

        if fail < 20:
            pass
            fail += 1
        else:
            break

    count += 1
    time.sleep(5)

print('Getting info about series took overall %s seconds' % (time.time() - start_time_program))
with open('Series.json', 'w') as f:
    json.dump(dictionary, f)
