import pandas as pd
import importlib.resources as pkg_resources

xslt = pkg_resources.read_text(__package__, 'lastfm.xslt')


def lastfm_to_ods(lastfm_file):
    lastfm_ods = lastfm_file.append('.ods')
    if lastfm_file.endswith('.csv'):  # works fine
        data = pd.read_csv(lastfm_file)
    elif lastfm_file.endswith('.json'):  # doesn't work at all
        data = pd.read_json(lastfm_file)
    elif lastfm_file.endswith('.xml'):
        data = pd.read_xml(lastfm_file, stylesheet=xslt)
    else:  # this shouldn't happen.
        return -1
    print(data.columns)
    data.to_excel(lastfm_ods, index=False)
    return lastfm_ods
