# jellyfin_to_ods()
# tautulli_to_ods()
# import_listens(tautulli_ods, "Tautulli") it works!
# (e)y(e)s w/o a %brain% (Eternal Home) should return Eternal Home
# Mr. Self Destruct (The Downward Spiral (deluxe edition)) should return The Downward Spiral (deluxe edition)

# Make sure to change to 'from .argparser import parse_args' when uploading
from .argparser import parse_args
import json
import os


def get_version():
    return "0.0.1"


def get_api_token(config):
    api_token = config['api_token']
    return api_token


def set_config(config):
    if config is None:
        config = os.path.expanduser('~') + "/config_listenbrainz.json"
    try:
        config = json.load(open(config))
    except FileNotFoundError:
        token = input("Enter in your ListenBrainz API Token (https://listenbrainz.org/profile/): ")
        json_config = {
            "api_token": token
        }
        with open(config, 'w+') as f:
            json.dump(json_config, f)
    # returns config as dict
    return config


def main():
    args = parse_args()
    file = args.file
    config = set_config(args.config)
    api_token = get_api_token(config)
    print(api_token)
