import pandas as pd


def rockbox_to_ods(rockbox_file):
    rockbox_ods = rockbox_file.replace(".log", ".ods")
    # maybe take advantage of line 2: timezone ?
    # although it appears to be a UNIX timestamp, so that shouldn't affect it
    # also I have no idea what rating does (L or S) so I'm dropping it for now
    data = pd.read_csv(rockbox_file, sep='\t', skiprows=(0, 1, 2),
                       names=["artist_name", "release_name", "track_name", "tracknumber", "duration", "rating",
                              "listened_at", "track_mbid"])
    data.drop('rating', axis=1, inplace=True)
    # just in case (one of the examples was missing release_name)
    # redundant (data = data.loc AND data = data.dropna)
    # will need to test the other parsers with dropna, didn't know that function existed at the time
    data = data.loc[data['artist_name'] != '']
    data = data.loc[data['release_name'] != '']
    data = data.loc[data['track_name'] != '']
    data = data.dropna(subset=["artist_name", "release_name", "track_name"])
    data.to_excel(rockbox_ods, index=False)
    return rockbox_ods, data
