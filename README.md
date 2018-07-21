# spdown
![status-dev](https://img.shields.io/badge/status-dev-yellow.svg)
![version-1-0-0](https://img.shields.io/badge/version-1.0.0-blue.svg)

A tool for downloading Spotify playlists from YouTube.

## Getting Started

### Dependencies
 * [ffmpeg](https://www.ffmpeg.org/)
 * [youtube-dl](https://github.com/rg3/youtube-dl)
 * [eyed3](https://github.com/nicfit/eyeD3)
 * [spotipy](https://github.com/plamere/spotipy)
 * [google-api-python-client](https://github.com/google/google-api-python-client)

__Don't forget to include _ffmpeg_ to your PATH__

### Installation

#### Using pip

    pip install --upgrade spdown

#### Using easy_install

    easy_install spdown

#### Manually

    python setup.py install

### Usage

    usage: spdown [-h] [--config CONFIG] [--secrets SECRETS] spotify_uri

    Downloads public Spotify playlists from YouTube
    
    positional arguments:
      spotify_uri        Spotify Playlist URI to download
    
    optional arguments:
      -h, --help         show this help message and exit
      --config CONFIG    Configuration File
      --secrets SECRETS  Spotify and Youtube API Secrets File

## Versioning
We use [SemVer](http://semver.org) for versioning. For the versions available, see the
tags on this repository.

## Authors
 * __Berke Emrecan Arslan__ - _initial work_ - [beremaran.com](https://beremaran.com)
 
## License
This project is licensed under the MIT license - see the [LICENSE](LICENSE) for details.