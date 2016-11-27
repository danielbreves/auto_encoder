# AutoEncoder
A python script to automatically encode media in a specified directory.

Usage:
`python3 encoder.py [-i <input_dir>] [-o <output_dir>] [--debug] [--dry] [--watch]`

## Dependencies
- [Python 3.x](https://www.python.org)
- [FFmpeg](https://www.google.com.au/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwj2_IWDr8XQAhUJUZQKHd-2BB0QFggZMAA&url=https%3A%2F%2Fwww.ffmpeg.org%2F&usg=AFQjCNE0r3Wi1_Kpr9JhvUfDFBerSxTW1g&bvm=bv.139782543,d.dGo)
- [Watchdog](https://github.com/gorakhargosh/watchdog)

## Installation

- `brew install ffmpeg`
- `pip install -r requirements.txt`

## Configuration
Change configuration constants in config.py.

## Options

`--debug`

Encodes only the first 15 seconds of each file.

`--dry`

Logs the output of each encoding command without actually encoding.

`--watch`

Watches for changes in the input directory.
