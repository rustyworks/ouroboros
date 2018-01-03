import shlex
import subprocess

from app.utils import seconds_to_time


class Prober(object):

    def __init__(self, file_location):
        self.file_location = file_location

    def get_video_duration(self):
        cmd = 'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {file_location}'.format(file_location=self.file_location)
        probe_cmd = shlex.split(cmd)
        raw_output = subprocess.check_output(probe_cmd).decode('utf-8').strip()
        duration = 0

        try:
            duration = float(raw_output)
        except ValueError as e:
            duration = 0
        return duration

    def generate_frame(self, number_of_frames, duration):
        # Use n + 1
        split_duration = duration // (number_of_frames + 1)
        capture_duration = split_duration
        for frame in range(number_of_frames):
            time = seconds_to_time(capture_duration)
            cmd = "ffmpeg -i {file_location} -ss {time} -f image2 -vframes 1 {file_location}_{frame}.png".format(file_location=self.file_location, frame=frame, time=time)
            print(cmd)
            capture_frame_cmd = shlex.split(cmd)
            subprocess.call(capture_frame_cmd)
            capture_duration += split_duration

