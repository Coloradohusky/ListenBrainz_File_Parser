import pandas as pd
import sqlite3
import json
import requests
from pprint import pprint
import time
import sys

database_path = "path_to_dbfiles"
tautulli_db = database_path + '/TautulliData.db'
jellyfin_db = database_path + '/playback_reporting.db'
tautulli_ods = database_path + '/TautulliData.ods'
jellyfin_ods = database_path + '/playback_reporting.ods'

listenbrainz_token = 'Token ' + "redacted"


# data = pd.read_sql("SELECT * FROM sqlite_master", con)
def tautulli_to_ods():
    con = sqlite3.connect(tautulli_db)
    # print(pd.read_sql("SELECT * FROM sqlite_master", con))
    # print(pd.read_sql("SELECT * FROM sessions LIMIT 1", con).columns.values.tolist())
    data = pd.read_sql("SELECT title,parent_title,grandparent_title,year,media_type FROM "
                       "session_history_metadata", con)
    # adds start time to output (stop time is unhelpful)
    session_data = pd.read_sql("SELECT started FROM session_history", con)
    data = pd.concat([data, session_data], axis=1, join='inner')
    data = data.loc[data['media_type'] == 'track']
    data.drop('media_type', axis=1, inplace=True)
    data = data.rename(columns={"title": "track_name", "parent_title": "release_name",
                                "grandparent_title": "artist_name", "started": "listened_at"})
    data['year'] = data['year'].astype("str")
    print(data.head(15))
    data.to_excel(tautulli_ods, index=False)


def jellyfin_to_ods():
    con = sqlite3.connect(jellyfin_db)
    print(pd.read_sql("SELECT * FROM PlaybackActivity LIMIT 1", con).columns.values.tolist())
    # will need to split ItemName into %artist_name% - %track_name% (%release_name%)
    data = pd.read_sql("SELECT DateCreated,ItemType,ItemName,PlayDuration FROM PlaybackActivity", con)
    data = data.loc[data['ItemType'] == 'Audio']
    data = data.loc[data['PlayDuration'] != 0]
    # edge case: Nine Inch Nails - Mr. Self Destruct (The Downward Spiral (deluxe edition))
    # better edge case: (e)y(e)s w/o a %brain% (Eternal Home)
    # (anything with the parentheses inside the parentheses)
    data[['artist_name', 'ItemName']] = data['ItemName'].str.split(pat=' - ', n=1, expand=True)
    # example 2022-08-01 20:34:33.5860918
    data['listened_at'] = pd.to_datetime(data['DateCreated'], format="%Y-%m-%d %H:%M:%S").astype("int64")
    data['listened_at'] = data['listened_at'].astype("str").str[:-9]
    # a really hacky way to convert from PST/PDT to UTC (adds 25200 seconds, or 7 hours)
    data['listened_at'] = data['listened_at'].astype("int64") + 25200
    print(data.info())
    data.drop(['ItemType', 'DateCreated'], axis=1, inplace=True)
    data = data.rename(columns={"PlayDuration": "duration"})
    data.to_excel(jellyfin_ods, index=False)


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


# jellyfin_to_ods()
# tautulli_to_ods()
# import_listens(tautulli_ods, "Tautulli") it works!
# (e)y(e)s w/o a %brain% (Eternal Home) should return Eternal Home
# Mr. Self Destruct (The Downward Spiral (deluxe edition)) should return The Downward Spiral (deluxe edition)
