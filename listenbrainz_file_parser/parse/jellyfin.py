import sqlite3
import pandas as pd


def jellyfin_to_ods(jellyfin_db):
    jellyfin_ods = jellyfin_db.replace(".db", ".ods")
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