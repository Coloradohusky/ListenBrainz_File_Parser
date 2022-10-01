from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser(description="Parses lists of listened music and uploads to ListenBrainz.")
    parser.add_argument("file")
    parser.add_argument(
        "--config",
        help=(
            "Manually specify config file. Default is ~/config_listenbrainz.json "
        )
    )
    parser.add_argument(
        "--max-batch",
        help=(
            "Maximum number of listens to import per batch"
        )
    )
    parser.add_argument(
        "--max-total",
        help=(
            "Maximum number of listens to import, in total."
        )
    )
    parser.add_argument(
        "--timeout",
        help=(
            "Number of seconds to wait between batches."
        )
    )

    args = parser.parse_args()
    return args
