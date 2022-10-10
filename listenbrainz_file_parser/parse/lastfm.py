import pandas as pd
import importlib.resources as pkg_resources
import json

xslt = pkg_resources.read_text(__package__, 'lastfm.xslt')


def lastfm_to_ods(lastfm_file):
    lastfm_ods = lastfm_file + '.ods'
    if lastfm_file.endswith('.csv'):
        data = pd.read_csv(lastfm_file)
    elif lastfm_file.endswith('.json'):
        # splits file into a list of around 200 JSONs per line
        json_list = json.load(open(lastfm_file, encoding='utf-8'))
        # print(json_list)
        data = pd.DataFrame()
        for i in json_list:
            for j in i:
                print(j)
                data.append(pd.DataFrame.from_dict(j))
        print(data.head())
        print(data.columns)
    elif lastfm_file.endswith('.xml'):
        data = pd.read_xml(lastfm_file, stylesheet=xslt)
    else:  # this shouldn't happen.
        return -1
    print(data.columns)
    print(data.head())
    data.to_excel(lastfm_ods, index=False)
    return lastfm_ods
