import pandas as pd


def lastfm_to_ods(lastfm_file):
    if lastfm_file.endswith('.csv'):  # works fine
        lastfm_ods = lastfm_file.replace(".csv", ".ods")
        data = pd.read_csv(lastfm_file)
    elif lastfm_file.endswith('.json'):  # doesn't work at all
        lastfm_ods = lastfm_file.replace(".csv", ".ods")
        data = pd.read_json(lastfm_file)
    elif lastfm_file.endswith('.xml'):  # mbid needs fixing
        lastfm_ods = lastfm_file.replace(".xml", ".ods")
        data = pd.read_xml(lastfm_file)
    else:  # this shouldn't happen.
        return -1
    print(data.head())
    # data.to_excel(lastfm_ods, index=False)
    return lastfm_ods
