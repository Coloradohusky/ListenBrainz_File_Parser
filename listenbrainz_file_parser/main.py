# jellyfin_to_ods()
# tautulli_to_ods()
# (e)y(e)s w/o a %brain% (Eternal Home) should return Eternal Home
# Mr. Self Destruct (The Downward Spiral (deluxe edition)) should return The Downward Spiral (deluxe edition)

from .argparser import parse_args
import json
import os
import sqlite3
import pandas as pd

from .parse.jellyfin import jellyfin_to_ods
from .parse.lastfm import lastfm_to_ods
from .parse.rockbox import rockbox_to_ods
from .parse.tautulli import tautulli_to_ods
from .submit.submit import import_listens


def get_version():
    return "0.0.4"


def set_config(config):
    if config is None:
        config = os.path.expanduser('~') + "/config_listenbrainz.json"
    try:
        config = json.load(open(config))
    except FileNotFoundError:
        token = input("Enter in your ListenBrainz API Token (https://listenbrainz.org/profile/): ")
        max_batch = input("Enter in how many listens you want to send per request (default 200): ")
        max_total = input("Enter in how many listens you want to send in total (default all): ")
        timeout = input("Enter in how many seconds you wish to wait between requests (default 3s): ")
        if max_batch == '':
            max_batch = 200
        if max_total == '':
            max_total = -1
        if timeout == '':
            timeout = 3
        json_config = {
            "api_token": token,
            "max_batch": max_batch,
            "max_total": max_total,
            "timeout": timeout
        }
        with open(config, 'w+') as f:
            json.dump(json_config, f)
        config = json.load(open(config))
    # returns config as dict
    return config


def detect_filetype(file, api_token, max_batch, max_total, timeout):
    if "/" in file:
        stripped_file = file.split("/")[-1]
    elif "\\" in file:
        stripped_file = file.split("\\")[-1]
    else:
        stripped_file = file
    print(stripped_file)
    if file.endswith('.db'):
        con = sqlite3.connect(file)
        value = (pd.read_sql("SELECT * FROM sqlite_master", con).values.tolist()[0][1])
        if value == 'version_info':
            media_player = 'Tautulli'
            ods = tautulli_to_ods(file)
        elif value == 'PlaybackActivity':
            media_player = 'Jellyfin'
            ods = jellyfin_to_ods(file)
        else:
            print('Filetype not currently supported.')
            return -1
    # a very weak way to detect Last.FM filetype, but oh well
    elif stripped_file.startswith('scrobbles-'):
        media_player = 'Last.FM'
        ods = lastfm_to_ods(file)
    elif stripped_file.endswith('.log'):
        media_player = 'RockBox'
        ods = rockbox_to_ods(file)
    else:
        print('Filetype not currently supported.')
        return -1

    import_listens(ods, media_player, api_token, max_batch, max_total, timeout)


def main():
    args = parse_args()
    file = args.file
    config = set_config(args.config)
    
    if args.api_token is None:
        api_token = config.get('api_token')
    else:
        api_token = args.api_token

    if args.max_batch is None:
        max_batch = int(config.get('max_batch'))
    else:
        max_batch = int(args.max_batch)

    if args.max_total is None:
        max_total = int(config.get('max_total'))
    else:
        max_total = int(args.max_total)

    if args.timeout is None:
        timeout = int(config.get('timeout'))
    else:
        timeout = int(args.timeout)

    detect_filetype(file, api_token, max_batch, max_total, timeout)
