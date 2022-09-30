# jellyfin_to_ods()
# tautulli_to_ods()
# import_listens(tautulli_ods, "Tautulli") it works!
# (e)y(e)s w/o a %brain% (Eternal Home) should return Eternal Home
# Mr. Self Destruct (The Downward Spiral (deluxe edition)) should return The Downward Spiral (deluxe edition)

# Make sure to change to 'from .argparser import parse_args' when uploading
from argparser import parse_args


def get_version():
    return "0.0.1"


def main():
    args = parse_args()
    file = args.file
    config = args.config
    print(config)
