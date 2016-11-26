"""
Source: https://trac.ffmpeg.org/wiki/Encode/H.264
"""
import os
import sys
import getopt
import subprocess

USAGE_INFO = 'python3 encode.py -i <input_dir> -o <output_dir> [--debug] [--dry]'
FFMPEG_PATH = '/usr/local/bin/ffmpeg'

VIDEO_CODEC = 'h264'
VIDEO_ENCODER = 'h264_omx'

AUDIO_CODEC = 'aac'
AUDIO_ENCODER = 'aac'

BITRATE = '2500k'

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

def walk_src_media(src_dir, callback):
    """get a sorted list of files that have a valid input extension"""
    for root, _dirs, files in os.walk(os.path.expanduser(src_dir)):
        for filename in files:
            if os.path.splitext(filename)[1] in INPUT_EXTS:
                callback(root, filename)

def encode(root, filename, src_dir, dest_dir, dry_run=False, debug=False):
    """encode file using ffmpeg"""
    input_filename = os.path.join(root, filename)
    path_to_create = os.path.dirname(os.path.relpath(input_filename, src_dir))
    path_to_create = os.path.join(dest_dir, path_to_create)
    output_filename = os.path.join(path_to_create, os.path.splitext(filename)[0] + OUTPUT_EXT)

    if os.path.isfile(output_filename):
        return

    command = [FFMPEG_PATH, '-i', os.path.expanduser(input_filename)]

    v_encoder = 'copy' if stream_codec('v:0', input_filename) == VIDEO_CODEC else VIDEO_ENCODER
    command += ['-c:v', v_encoder]

    a_encoder = 'copy' if stream_codec('a:0', input_filename) == AUDIO_CODEC else AUDIO_ENCODER
    command += ['-c:a', a_encoder]

    command += ['-b:v', BITRATE]

    if debug:
        command += ['-to', '15']

    command += [os.path.expanduser(output_filename)]

    print('\n', ' '.join(command), '\n')

    if not dry_run:
        os.makedirs(path_to_create, exist_ok=True)
        subprocess.call(command)

def main(argv):
    """main function executed when running from the command-line"""
    in_dir = os.getcwd()
    out_dir = os.getcwd()
    dry = False
    debug = False

    try:
        opts, _args = getopt.getopt(argv, "hi:o:", ["debug", "dry", "input=", "output="])
    except getopt.GetoptError:
        print(USAGE_INFO)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(USAGE_INFO)
            sys.exit()
        elif opt in ("-i", "--input"):
            in_dir = arg
        elif opt in ("-o", "--output"):
            out_dir = arg
        elif opt == '--dry':
            dry = True
        elif opt == '--debug':
            debug = True

    walk_src_media(in_dir, lambda root, filename: encode(root, filename, in_dir, out_dir, dry_run=dry, debug=debug))

if __name__ == "__main__":
    main(sys.argv[1:])
