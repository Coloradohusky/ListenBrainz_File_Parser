import pandas as pd
import json
import ast
import datetime
import progressbar as pb


def spotify_to_ods(spotify_file):
    spotify_ods = spotify_file + '.ods'
    if spotify_file.endswith('.json'):
        json_list = json.load(open(spotify_file, encoding='utf-8'))
        data = pd.DataFrame()
        for i in pb.progressbar(json_list, prefix=spotify_file):
            if i["incognito_mode"] or i["master_metadata_track_name"] is None or i["master_metadata_track_name"] is None or i["master_metadata_track_name"] is None:
                continue
            i["ts"] = datetime.datetime.strptime(i["ts"], "%Y-%m-%dT%H:%M:%SZ").timestamp()
            json_i = ast.literal_eval(str(i))
            data = pd.concat([data, pd.json_normalize(json_i)])
        data.drop('conn_country', axis=1, inplace=True)
        data.drop('ip_addr_decrypted', axis=1, inplace=True)
        data.drop('user_agent_decrypted', axis=1, inplace=True)
        data.drop('username', axis=1, inplace=True)
        data = data.rename(
            columns={"master_metadata_track_name": "track_name", "master_metadata_album_album_name": "release_name",
                     "master_metadata_album_artist_name": "artist_name", "ts": "listened_at"})
        print(data)

    else:  # this shouldn't happen... right?
        return -1
    print(f"Exporting to {spotify_ods}...")
    data.to_excel(spotify_ods, index=False)
    return spotify_ods, data
