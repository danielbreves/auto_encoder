"""
Source: https://trac.ffmpeg.org/wiki/Encode/H.264
"""
import os
import sys
import subprocess

FFMPEG_PATH = '/usr/local/bin/ffmpeg'

VIDEO_CODEC = 'h264'
VIDEO_ENCODER = 'h264_omx'

AUDIO_CODEC = 'aac'
AUDIO_ENCODER = 'aac'

BITRATE = '2500k'

SRC_DIR = os.path.expanduser('~/Desktop')
DEST_DIR = os.path.expanduser('~/Desktop/Media')

INPUT_EXTS = ['.mkv']
OUTPUT_EXT = '.mp4'

def stream_codec(stream, filename):
    """return the codec name for a stream"""
    return subprocess.check_output([
        'ffprobe',
        '-v',
        'error',
        '-select_streams',
        stream,
        '-show_entries',
        'stream=codec_name',
        '-of',
        'default=nokey=1:noprint_wrappers=1',
        filename
    ])

def walk_src_media(callback):
    """get a sorted list of files that have a valid input extension"""
    for root, _dirs, files in os.walk(os.path.expanduser(SRC_DIR)):
        for filename in files:
            if os.path.splitext(filename)[1] in INPUT_EXTS:
                callback(root, filename)

def encode(root, filename, opts):
    """encode file using ffmpeg"""
    input_filename = os.path.join(root, filename)
    path_to_create = os.path.dirname(os.path.relpath(input_filename, SRC_DIR))
    path_to_create = os.path.join(DEST_DIR, path_to_create)
    output_filename = os.path.join(path_to_create, os.path.splitext(filename)[0] + OUTPUT_EXT)

    if os.path.isfile(output_filename):
        return

    command = [FFMPEG_PATH, '-i', os.path.expanduser(input_filename)]

    v_encoder = 'copy' if stream_codec('v:0', input_filename) == VIDEO_CODEC else VIDEO_ENCODER
    command += ['-c:v', v_encoder]

    a_encoder = 'copy' if stream_codec('a:0', input_filename) == AUDIO_CODEC else AUDIO_ENCODER
    command += ['-c:a', a_encoder]

    command += ['-b:v', BITRATE]

    if '--debug' in opts:
        command += ['-to', '15']

    command += [os.path.expanduser(output_filename)]

    if '--dry' in opts:
        print(' '.join(command), '\n')
    else:
        os.makedirs(path_to_create, exist_ok=True)
        subprocess.run(command)

def process(args):
    """encode media from the source directory into the destination directory"""
    walk_src_media(lambda root, filename: encode(root, filename, args))

if __name__ == "__main__":
    process(sys.argv[1:])
