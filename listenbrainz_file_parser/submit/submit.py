import pandas as pd
import json
import requests
import time
import sys


def submit_to_listenbrainz(payload):
    listenbrainz_submit = {
        "listen_type": "import",
        "payload": payload
    }
    listenbrainz_submit = json.dumps(listenbrainz_submit)
    r = requests.post("https://api.listenbrainz.org/1/submit-listens",
                      headers={'Authorization': listenbrainz_token}, data=listenbrainz_submit)
    print(r)
    print(r.json())
    if r.json()['status'] != 'ok':
        sys.exit()
    time.sleep(3) # just a guess
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
                "submission_client": "DataBase Listen Uploader by Coloradohusky",
            }
        }
    }
    for arg in listen_series.index:
        if (arg not in ['release_name', 'track_name', 'artist_name', 'listened_at']) and \
                (listen_series[arg] is True):
            listen_json['track_metadata']['additional_info'][arg] = listen_series[arg]
    return listen_json


def import_listens(file, media_player):
    data = pd.read_excel(file, dtype="str")
    print(data.dtypes)
    # how many listens to submit to ListenBrainz at once
    listen_chunk = 200
    for i in range(0, int(len(data) / listen_chunk) + 1):
        data_chunk = (data[i * listen_chunk:(i * listen_chunk) + listen_chunk])
        payload = make_payload(data_chunk, media_player)
        submit_to_listenbrainz(payload)
    print('Done')