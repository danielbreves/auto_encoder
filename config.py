FFMPEG_PATH = '/usr/local/bin/ffmpeg'

VIDEO_CODEC = 'h264' # used with ffprobe to detect whether or not we need to encode
VIDEO_ENCODER = 'h264_omx'

AUDIO_CODEC = 'aac' # used with ffprobe to detect whether or not we need to encode
AUDIO_ENCODER = 'aac'

BITRATE = '2500k'

INPUT_EXTS = ['.mkv', '.mp4', '.avi']
OUTPUT_EXT = '.mp4'
