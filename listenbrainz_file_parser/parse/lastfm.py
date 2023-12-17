import pandas as pd
import importlib.resources as pkg_resources
import json
import ast

xslt = pkg_resources.read_text(__package__, 'lastfm.xslt')


def lastfm_to_ods(lastfm_file):
    lastfm_ods = lastfm_file + '.ods'
    if lastfm_file.endswith('.csv'):
        data = pd.read_csv(lastfm_file)
        data.drop('utc_time', axis=1, inplace=True)
        data = data.rename(columns={"track": "track_name", "album": "release_name", "artist": "artist_name",
                                    "uts": "listened_at", "album_mbid": "release_mbid"})
    elif lastfm_file.endswith('.json'):
        # splits file into a list of around 200 JSONs per line
        json_list = json.load(open(lastfm_file, encoding='utf-8'))
        # print(json_list)
        data = pd.DataFrame()
        for i in json_list:
            json_i = ast.literal_eval(str(i))
            data = pd.concat([data, pd.json_normalize(json_i)])
        data.drop('image', axis=1, inplace=True)
        data.drop('streamable', axis=1, inplace=True)
        data.drop('date.#text', axis=1, inplace=True)
        data = data.rename(columns={"name": "track_name", "album.#text": "release_name",
                                    "artist.#text": "artist_name", "date.uts": "listened_at",
                                    "mbid": "track_mbid", "artist.mbid": "artist_mbid",
                                    "album.mbid": "release_mbid", "url": "origin_url"})
    elif lastfm_file.endswith('.xml'):
        data = pd.read_xml(lastfm_file, stylesheet=xslt)
        data = data.rename(columns={"name": "track_name", "album": "release_name", "artist": "artist_name",
                                    "utc": "listened_at", "album_mbid": "release_mbid", "url": "origin_url"})
    else:  # this shouldn't happen... right?
        return -1
    data.to_excel(lastfm_ods, index=False)
    return lastfm_ods, data
