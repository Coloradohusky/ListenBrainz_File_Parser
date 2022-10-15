import pandas as pd
import json
import requests
import time
import sys


def submit_to_listenbrainz(payload, api_token, timeout):
    listenbrainz_submit = {
        "listen_type": "import",
        "payload": payload
    }
    listenbrainz_submit = json.dumps(listenbrainz_submit)
    r = requests.post("https://api.listenbrainz.org/1/submit-listens",
                      headers={'Authorization': 'Token ' + api_token}, data=listenbrainz_submit)
    print(r)
    print(r.json())
    try:
        if r.json()['status'] != 'ok':
            sys.exit()
    except KeyError:
        # if there's an error (503, 400, etc.) it will print some of the last chunk of data
        # so that the user can format their data as to not resubmit the same track twice
        # (not that ListenBrainz cares, they handle dupes well)
        print(json.dumps(listenbrainz_submit)[:300])
        sys.exit()
    time.sleep(timeout)
    return 0


def make_payload(data_chunk, media_player):
    # yes, I know I shouldn't do iterrows, but I don't know what other option to do atm
    payload = []
    for row in data_chunk.iterrows():
        payload.append(make_listen(row[1], media_player))
    return payload


def make_listen(listen_series, media_player):
    listen_json = {
        "listened_at": listen_series['listened_at'],
        "track_metadata": {
            "artist_name": listen_series['artist_name'],
            "track_name": listen_series['track_name'],
            "release_name": listen_series['release_name'],
            "additional_info": {
                "media_player": media_player,
                # would like to add get_version to submission_client, but gives me a circular import
                "submission_client": "ListenBrainz File Parser by Coloradohusky",
            }
        }
    }
    for arg in listen_series.index:
        # NaNs are floats, not NoneType
        # might cause issues in the future with genuine floats, but try to keep things as ints I guess
        if (arg not in ['release_name', 'track_name', 'artist_name', 'listened_at']) and \
                (not isinstance(listen_series[arg], float)):
            listen_json['track_metadata']['additional_info'][arg] = listen_series[arg]
    return listen_json


def import_listens(file, media_player, api_token, max_batch, max_total, timeout):
    data = pd.read_excel(file, dtype="str")
    # how many listens to submit to ListenBrainz at once
    if max_total == -1:
        max_total = len(data) + 1
    for i in range(0, int(max_total / max_batch) + 1):
        data_chunk = (data[i * max_batch:min((i * max_batch) + max_batch, max_total)])
        payload = make_payload(data_chunk, media_player)
        submit_to_listenbrainz(payload, api_token, timeout)
    print('Done')
