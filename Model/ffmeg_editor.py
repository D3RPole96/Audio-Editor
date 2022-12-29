import re
import subprocess

import ffmpeg
import math

from Model.fragment import Fragment


def concat(fragments, output_path):
    files = []
    for fragment in fragments:
        files.append(ffmpeg.input(fragment).audio)
    (
        ffmpeg
        .concat(*files, a=1, v=0)
        .output(output_path)
        .run()
    )

def trim(path, output_path, start, end):
    (
        ffmpeg
        .input(path)
        .filter_('atrim', start = start, end = end)
        .output(output_path)
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


def __get_length(file):
    cmd = 'ffprobe -i {} -show_entries format=duration -v quiet -of csv="p=0"'.format(file)
    output = subprocess.check_output(
        cmd,
        shell=True,
        stderr=subprocess.STDOUT
    )

    return float(output)


def get_duration(file):
    try:
        seconds = math.floor(__get_length(file))

        return f'{seconds // 60}:{"0" if seconds % 60 < 10 else ""}{seconds % 60}'
    except:
        return ''


def get_duration_with_percent(file, percent):
    seconds = math.floor(__get_length(file) * percent)

    return f'{seconds // 60}:{"0" if seconds % 60 < 10 else ""}{seconds % 60}'
