# Listenbrainz File Parser
 Parses database files from different music listen tracker applications, and imports them into [ListenBrainz](https://listenbrainz.org/)

## Installation
 Download and extract the zip, then run `python -m pip install -e "\path\to\folder"`.

## Usage
```
listenbrainz_file_parser [-h] [--config CONFIG] [--max-batch MAX_BATCH] [--max-total MAX_TOTAL]
                         [--timeout TIMEOUT] [--api-token API_TOKEN]
                         file

Parses lists of listened music and uploads to ListenBrainz.

positional arguments:
  file

options:
  -h, --help            Show this help message and exit.
  --config CONFIG       Manually specify config file. Default is ~/config_listenbrainz.json.
  --max-batch MAX_BATCH
                        Maximum number of listens to import per batch. Overrides config.
  --max-total MAX_TOTAL
                        Maximum number of listens to import, in total. Overrides config.
  --timeout TIMEOUT     Number of seconds to wait between batches. Overrides config.
  --api-token API_TOKEN
                        Specify your ListenBrainz API Token (https://listenbrainz.org/profile/). Overrides config.
```

## List of Music Trackers

### Working
#### [Plex](https://www.plex.tv/) / [Tautulli](https://tautulli.com/)
- `tautulli.db`
#### [last.fm](https://www.last.fm/home) / [mainstream.ghan.nl](https://mainstream.ghan.nl/export.html)
- `scrobbles-*.csv`
- `scrobbles-*.json`
- `scrobbles-*.xml`
#### [RockBox](https://community.metabrainz.org/t/dealing-with-scrobbler-log-files/)
- `.scrobbler.log`
#### [Jellyfin](https://jellyfin.org/) / [Playback Reporting Plugin](https://github.com/jellyfin/jellyfin-plugin-playbackreporting)
- `playback_reporting.db`

### In Progress
None

### Planned
#### [snd.wave (iOS)](https://sndwave.app/)
#### [SongStats (iOS)](https://apps.apple.com/us/app/song-stats-for-apple-music/id1450329823)
#### 

### Send in suggestions, with attached files!
