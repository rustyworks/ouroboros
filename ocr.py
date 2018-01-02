import argparse
import os
import re
import shlex
import subprocess
import sys

import pytesseract
import cv2

from PIL import Image

def check_video_duration(file_location):
    cmd = 'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {file_location}'.format(file_location=file_location)
    probe_cmd = shlex.split(cmd)
    raw_output = subprocess.check_output(probe_cmd).decode('utf-8').strip()
    duration = 0

    try:
        duration = float(raw_output)
    except ValueError as e:
        duration = 0
    return duration

def capture_frame(file_location, number_of_frames, duration):
    # Use n + 1
    split_duration = duration // (number_of_frames + 1)
    capture_duration = split_duration
    for frame in range(number_of_frames):
        time = seconds_to_time(capture_duration)
        cmd = "ffmpeg -i {file_location} -ss {time} -f image2 -vframes 1 {file_location}_{frame}.png".format(file_location=file_location, frame=frame, time=time)
        print(cmd)
        capture_frame_cmd = shlex.split(cmd)
        subprocess.call(capture_frame_cmd)
        capture_duration += split_duration

def seconds_to_time(seconds):
    seconds = int(seconds)
    return '{hours:02d}:{minutes:02d}:{seconds:02d}'.format(hours=(seconds // 60), minutes=(seconds // 60 % 60), seconds=(seconds % 60))

def check_text(image_location):
    image = cv2.imread(image_location)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    file_location = '{}.png'.format(os.getpid())
    cv2.imwrite(file_location, gray)

    text = pytesseract.image_to_string(Image.open(file_location))
    os.remove(file_location)
    print(text)

    cv2.imshow('Image', image)
    cv2.imshow('Output', gray)
    cv2.waitKey(0)
    return text

def check_spam(text):
    return is_phone_num(text) or is_link(text) or is_banned_words(text)

def is_phone_num(text):
    pattern = '\(?([0-9]{3,4})\)?[-.●]?([0-9]{3,4})[-.●]?([0-9]{3,4})'
    return True

def is_link(text):
    pattern = '[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
    return re.search(pattern, text)

def is_banned_words(text):
    pattern = '(jual|beli|www)'
    return re.search(pattern, text)

def clean_up_text(text):
    pattern = '\W+'
    return re.sub(pattern, '', text)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--file-location', required=True, help="path to input video to be OCR'd")
    ap.add_argument('-n', '--number-frames', default=5, type=int, help="number of frames")
    args = vars(ap.parse_args())

    file_location = args['file_location']
    number_of_frames = args['number_frames']

    duration = check_video_duration(file_location)
    capture_frame(file_location, number_of_frames, duration)

    is_spam = False
    for frame in range(number_of_frames):
        image_name = '{file_location}_{frame}.png'.format(file_location=file_location, frame=frame)
        text = check_text(image_name)
        clean_text = clean_up_text(text)
        is_spam = is_spam or check_spam(clean_text)
    print('Ini adalah: {status}'.format(status='Spam' if is_spam else 'Ham'))
    sys.exit(1)

