#!/usr/bin/env python

"""
Split long MP3 file into multiple MP3 files at its chapter marks.

Based on: https://github.com/Mortal/chaptersplit
"""

import os
import collections
import shutil
import argparse
import subprocess
import json

EXTENSION = "mp3"
REQUIRED_PROGRAMS = {
    'ffprobe': 'ffmpeg',
    'ffmpeg': 'ffmpeg'
}

def check_required_programs():
    missing = collections.defaultdict(list)
    for program, package in REQUIRED_PROGRAMS.items():
        path = shutil.which(program)
        if path is None:
            missing[package].append(program)

    for package, programs in missing.items():
        print(("Required program%s %s not found. " +
               "Consider installing the %s package.") %
              ('' if len(programs) == 1 else 's',
               ', '.join(programs), package))

    if missing:
        raise SystemExit(1)

class Chapter:
    @staticmethod
    def from_json(json):
        return Chapter(json["start_time"], json["end_time"], json["tags"]["title"])

    def __init__(self, start_time, end_time, title):
        self.start_time = start_time
        self.end_time = end_time
        self.title = title

def chapters_from_json(from_json):
    all_chapters = from_json["chapters"]
    result = list(map(Chapter.from_json, all_chapters))

    # Check if end and start times align
    for ch_i, ch_j in zip(result[:-1], result[1:]):
        if ch_i.end_time != ch_j.start_time:
            raise Exception(
                "Chapters are not contiguous: %s != %s at end of %s" % (ch_i.end_time, ch_j.start_time, ch_i.title))

    return result

class Original:
    @staticmethod
    def parse(filename):
        metadata = subprocess.check_output(
                ['ffprobe',
                 '-v', 'quiet',
                 '-i', filename,
                 '-print_format', 'json',
                 '-show_format',
                 '-show_chapters'])
        metadata_json = json.loads(metadata)
        return Original(filename=filename,
                        artist=metadata_json["format"]["tags"]["artist"],
                        album=metadata_json["format"]["tags"]["album"],
                        chapters=chapters_from_json(metadata_json))

    def __init__(self, filename, artist, album, chapters):
        self.filename = filename
        self.artist = artist
        self.album = album
        self.chapters = chapters

    def extract_chapters(self, out_path, verbose=False):
        fname_base = "%s - %s" % (self.artist, self.album)
        for num, chapter in enumerate(self.chapters, start=1):
            chapter_filename = "%03d %s - %s.%s" % (num, fname_base, chapter.title, EXTENSION)
            chapter_path = os.path.join(out_path, chapter_filename)
            if verbose:
                print("Processing %s (%i/%i)..." % (chapter_path, num, len(self.chapters)))
            subprocess.run(
                ['ffmpeg',
                 '-v', 'quiet',
                 '-i', self.filename,
                 '-ss', chapter.start_time,
                 '-to', chapter.end_time,
                 '-id3v2_version', '3',
                 '-metadata:s:v', 'title="Album cover"',
                 '-metadata:s:v', 'comment="Cover (front)"',
                 '-c', 'copy',
                 chapter_path])

def main():
    parser = argparse.ArgumentParser(description="""
        Split an MP3 file into MP3 files based on the embedded chapters.
        Uses shellouts to ffmpeg to do the processing. You
        """)
    parser.add_argument('-i', '--input-file', required=True)
    parser.add_argument('-o', '--output-dir', required=True)
    parser.add_argument('-v', '--verbose', action='store_true', required=False, help="Verbose output during file processing")

    try:
        args = parser.parse_args()
    finally:
        # If parse_args registers bad arguments,
        # we still want to give an error about missing programs.
        check_required_programs()

    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)

    Original.parse(args.input_file)\
            .extract_chapters(out_path=args.output_dir, verbose=args.verbose)

if __name__ == "__main__":
    main()
