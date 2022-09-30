from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser(description="Parses lists of listened music and uploads to ListenBrainz.")
    parser.add_argument("file")
    parser.add_argument(
        "--config",
        help=(
            "Manually specify config file. "
            "Default is ~/config_listenbrainz.json "
        ),
    )

    args = parser.parse_args()
    return args
