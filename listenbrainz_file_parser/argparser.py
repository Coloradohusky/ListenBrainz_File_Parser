from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser(description="Parses lists of listened music and uploads to ListenBrainz.")
    parser.add_argument("file")
    parser.add_argument(
        "--config",
        help=(
            "Manually specify config file. Default is ~/config_listenbrainz.json."
        )
    )
    parser.add_argument(
        "--max-batch",
        help=(
            "Maximum number of listens to import per batch. Overrides config."
        )
    )
    parser.add_argument(
        "--max-total",
        help=(
            "Maximum number of listens to import, in total. Overrides config."
        )
    )
    parser.add_argument(
        "--timeout",
        help=(
            "Number of seconds to wait between batches. Overrides config."
        )
    )
    parser.add_argument(
        "--api-token",
        help=(
            "Specify your ListenBrainz API Token (https://listenbrainz.org/profile/). Overrides config."
        )
    )

    args = parser.parse_args()
    return args
