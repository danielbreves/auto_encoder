"""
main script for AutoEncoder
"""
import os
import sys
import time
import getopt
import config
import utils
from encoder import encode
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileCreatedEvent

USAGE_INFO = 'python3 encode.py -i <input_dir> -o <output_dir> [--debug] [--dry] [--watch] [--delete-original]'

class MediaFolderEventHandler(FileSystemEventHandler):
    def __init__(self, in_dir, out_dir, options):
        self.in_dir = in_dir
        self.out_dir = out_dir
        self.opts = options

    def on_any_event(self, event):
        if isinstance(event, FileCreatedEvent) and is_media(event.src_path):
            utils.print_result('Media created: ' + event.src_path)
            encode(event.src_path, self.in_dir, self.out_dir, self.opts)

def is_media(filename):
    return os.path.splitext(filename)[1] in config.INPUT_EXTS

def walk_src_media(src_dir, callback):
    """get a sorted list of files that have a valid input extension"""
    for root, _dirs, files in os.walk(os.path.expanduser(src_dir)):
        for filename in files:
            if is_media(filename):
                callback(os.path.join(root, filename))

def main(argv):
    """main function executed when running from the command-line"""
    in_dir = os.getcwd()
    out_dir = os.getcwd()
    watch = False
    options = {
        'dry': False,
        'debug': False,
        'delete_original': False
    }

    try:
        opts, _args = getopt.getopt(argv, "hi:o:", ["watch", "debug", "dry", "delete-original", "input=", "output="])
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
            options['dry'] = True
        elif opt == '--debug':
            options['debug'] = True
        elif opt == '--delete-original':
            options['delete_original'] = True
        elif opt == '--watch':
            watch = True

    utils.print_result('Encoding existing media: ' + in_dir)
    walk_src_media(in_dir, lambda src_path: encode(src_path, in_dir, out_dir, options))

    if watch:
        utils.print_result('Watching: ' + in_dir)
        event_handler = MediaFolderEventHandler(in_dir, out_dir, options)
        observer = Observer()
        observer.schedule(event_handler, in_dir, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

if __name__ == "__main__":
    main(sys.argv[1:])
