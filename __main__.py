#!/usr/bin/env python3

# -*- coding:utf-8 -*-

import argparse
import html.parser
import json
import os
import re
import sys
import time
import urllib.request
import time

from colorama import init, Fore, Style
import modules
import color


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def main():
    init()
    crawl_new_torrent_only = False
    cron_job = True
    cron_job_interval = 2
    cls()
    while True:
        print('Ohys-Raws Crawler Engine 4.17\nPython Version\n\nDeveloped By Cryental\n')
        if not os.path.exists('torrents'):
            os.makedirs('torrents')
        if not os.path.exists('output'):
            os.makedirs('output')
        if crawl_new_torrent_only and cron_job:
            color.color_print(Fore.YELLOW, '[!]', 'CRONJOB SET: INTERVAL TO {} SEC'.format(cron_job_interval) + '\n')
            time.sleep(cron_job_interval)
        color.color_print(Fore.YELLOW, '[DONE]', 'READING HEADERS')
        color.color_print(Fore.YELLOW, '[DONE]', 'WEBCLIENT INIT')
        color.color_print(Fore.YELLOW, '[DONE]', 'SET NORMAL HEADERS')
        color.color_print(Fore.YELLOW, '[RUNNING]', 'TORRENT LIST LOADING\n')
        if crawl_new_torrent_only:
            color.color_print(Fore.YELLOW, '[DONE]', 'MODE SELECTED - NEW TORRENT ONLY MODE')
        else:
            color.color_print(Fore.YELLOW, '[DONE]', 'MODE SELECTED - FULL DUMP MODE')
        if not crawl_new_torrent_only:
            color.color_print(Fore.YELLOW, '[RUNNING]', 'NEW TORRENT LIST LOADING\n')
        color.color_print(Fore.YELLOW, '[RUNNING]', 'NEW TORRENT LIST LOADING')
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/80.0.3987.132 Safari/537.36"}
        cancel_crawling_state = False
        new_torrent_state = False
        try:
            for i in range(0, 150):
                req = urllib.request.Request('http://torrents.ohys.net/t/json.php?dir=disk&p={}'.format(str(i)),
                                             headers=headers)
                response = urllib.request.urlopen(req)
                contents = response.read()
                contents_array = json.loads(contents)
                if len(contents_array) == 0:
                    break
                for item in contents_array:
                    decoded_file_name = html.unescape(item['t'])
                    if not os.path.isfile('torrents\\' + decoded_file_name) or os.stat('torrents\\' + decoded_file_name).st_size == 0:
                        time.sleep(0.008)
                        urllib.request.urlretrieve('http://torrents.ohys.net/t/' + item['a'],
                                                   'torrents\\' + decoded_file_name)
                        color.color_print(Fore.YELLOW, '[DOWNLOADED]', decoded_file_name)
                        new_torrent_state = True
                    elif crawl_new_torrent_only:
                        cancel_crawling_state = True
                    else:
                        color.color_print(Fore.YELLOW, '[EXISTED]', decoded_file_name)
                if cancel_crawling_state:
                    break
        except:
            pass
        color.color_print(Fore.YELLOW, '[DONE]', 'TORRENT LOADED')
        if new_torrent_state:
            color.color_print(Fore.YELLOW, '[PROCESSING]', 'OUTPUT TO JSON TYPE')
            time.sleep(2)
            modules.database_builder()
            color.color_print(Fore.YELLOW, '[DONE]', 'OUTPUT TO JSON TYPE')
        if not cron_job:
            sys.exit(0)
            break
        cls()

if __name__ == "__main__":
    main()


