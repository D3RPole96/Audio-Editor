import re
import subprocess

import ffmpeg
import math

from Model.fragment import Fragment


def concat(fragments, output_path):
    files = []
    for fragment in fragments:
        files.append(ffmpeg.input(fragment.content).audio)
    (
        ffmpeg
        .concat(*files, a=1, v=0)
        .output(output_path[1:])
        .run()
    )


def reverse(path, output_path):
    (
        ffmpeg
        .input(path)
        .filter('areverse')
        .output(output_path)
        .run()
    )


def change_speed(path, output_path, speed_ratio):
    (
        ffmpeg
        .input(path)
        .filter('atempo', speed_ratio)
        .output(output_path)
        .run()
    )


def get_length(path):
    return '0:00:00'

    cmd = ['ffprobe', '-show_format', '-pretty', '-loglevel', 'quiet', path]
    info_byte = subprocess.check_output(cmd)
    info_str = info_byte.decode("utf-8")
    info_list = re.split('[\n]', info_str)
    for info in info_list:
        if 'duration' in info:
            duration = re.split('[=]', info)[1]
    return duration
