"""
Source: https://trac.ffmpeg.org/wiki/Encode/H.264
"""
import os
import subprocess
import re
import config
import utils

TV_SHOW_REGEX = re.compile(r".+S\d{2}E\d{2}.+")
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
TMP_DIR = os.path.join(CURRENT_DIR, 'tmp')

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
    ]).decode('ascii').strip()

def make_path(src_path, src_dir, dest_dir, dry_run=False):
    filename = os.path.basename(src_path)
    path_to_create = os.path.dirname(os.path.relpath(src_path, src_dir))

    cat_dir = 'TV Shows' if TV_SHOW_REGEX.match(src_path) else 'Movies'
    path_to_create = os.path.join(dest_dir, cat_dir, path_to_create)

    if not dry_run:
        os.makedirs(path_to_create, exist_ok=True)

    output_filename = os.path.join(path_to_create, os.path.splitext(filename)[0] + config.OUTPUT_EXT)
    return output_filename

def encode(src_path, src_dir, dest_dir, opts):
    """encode file using ffmpeg"""
    output_filename = make_path(src_path, src_dir, dest_dir, dry_run=opts['dry'])
    output_filename = os.path.expanduser(output_filename)

    os.makedirs(TMP_DIR, exist_ok=True)
    tmp_filename = os.path.join(TMP_DIR, os.path.basename(output_filename))

    if os.path.isfile(output_filename):
        utils.print_result('Skipping ' + output_filename + ', file already exists!')
        return

    command = [config.FFMPEG_PATH, '-i', os.path.expanduser(src_path)]

    v_encoder = 'copy' if stream_codec('v:0', src_path) == config.VIDEO_CODEC else config.VIDEO_ENCODER
    command += ['-c:v', v_encoder]

    a_encoder = 'copy' if stream_codec('a:0', src_path) == config.AUDIO_CODEC else config.AUDIO_ENCODER
    command += ['-c:a', a_encoder]

    command += ['-b:v', config.BITRATE]

    if opts['debug']:
        command += ['-to', '5']

    command += [tmp_filename]

    utils.print_result('Running: ' + ' '.join(command))

    if not opts['dry']:
        subprocess.call(command)
        utils.print_result('Moving: ' + tmp_filename + ' to: ' + output_filename)
        os.rename(tmp_filename, output_filename)
        if opts['delete_original']:
            utils.print_result('Deleting: ' + src_path)
            os.remove(src_path)
