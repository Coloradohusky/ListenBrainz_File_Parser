import sqlite3
import pandas as pd


def jellyfin_to_ods(jellyfin_db):
    jellyfin_ods = jellyfin_db.replace(".db", ".ods")
    con = sqlite3.connect(jellyfin_db)
    print(pd.read_sql("SELECT * FROM PlaybackActivity LIMIT 1", con).columns.values.tolist())
    data = pd.read_sql("SELECT DateCreated,ItemType,ItemName,PlayDuration FROM PlaybackActivity", con)
    data = data.loc[data['ItemType'] == 'Audio']
    data = data.loc[data['PlayDuration'] != 0]
    # grabs artist_name from ItemName
    data[['artist_name', 'ItemName']] = data['ItemName'].str.split(pat=' - ', n=1, expand=True)
    # grabs album and track_name from ItemName
    result = [split_itemname(x) for x in data['ItemName']]
    album_name = []
    track_name = []
    for i in result:
        album_name.append(i[0])
        track_name.append(i[1])
    data['release_name'] = album_name
    data['track_name'] = track_name
    # example 2022-08-01 20:34:33.5860918
    data['listened_at'] = pd.to_datetime(data['DateCreated'], format="%Y-%m-%d %H:%M:%S").astype("int64")
    data['listened_at'] = data['listened_at'].astype("str").str[:-9]
    # a really hacky way to convert from PST/PDT to UTC (adds 25200 seconds, or 7 hours)
    # will need to make more user-customizable, to allow for different timezones
    data['listened_at'] = data['listened_at'].astype("int64") + 25200
    print(data.info())
    data.drop(['ItemType', 'DateCreated', 'ItemName'], axis=1, inplace=True)
    data = data.rename(columns={"PlayDuration": "duration"})
    data.to_excel(jellyfin_ods, index=False)
    return jellyfin_ods


def split_itemname(item_name):
    song = item_name[::-1]
    parenthesis = 0
    for i in range(len(song)):
        if (song[i] != ")" and song[i] != "(") and parenthesis == 0:
            album_name = song[1:i - 1][::-1]
            track_name = song[i + 1:][::-1]
            break
        else:
            if song[i] == ")":
                parenthesis = parenthesis + 1
            elif song[i] == "(":
                parenthesis = parenthesis - 1
    return [album_name, track_name]