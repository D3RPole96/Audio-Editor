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
    length = math.ceil(float(ffmpeg.probe(path)['format']['duration']))
    return str(length // 60) + ' : ' + str(length % 60)
