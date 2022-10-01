import sqlite3
import pandas as pd


def tautulli_to_ods(tautulli_db):
    tautulli_ods = tautulli_db.replace(".db", ".ods")
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
    return tautulli_ods
