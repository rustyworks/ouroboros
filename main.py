import argparse
import sys

from app.checker import Checker
from app.ocr import OCR
from app.prober import Prober
from app.utils import seconds_to_time, delete_file


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file-location', required=True, help="path to input video to be OCR'd")
    parser.add_argument('-n', '--number-frames', default=5, type=int, help="number of frames")
    args = vars(parser.parse_args())

    file_location = args['file_location']
    number_of_frames = args['number_frames']

    prober = Prober(file_location)
    duration = prober.get_video_duration()
    prober.generate_frame(number_of_frames, duration)

    checker = Checker()
    is_spam = False
    for frame in range(number_of_frames):
        image_name = '{file_location}_{frame}.png'.format(file_location=file_location, frame=frame)
        ocr = OCR(image_name)
        text = ocr.to_text()
        is_spam = is_spam or checker.is_spam(text)
        delete_file(image_name)
    print('Ini adalah: {status}'.format(status='Spam' if is_spam else 'Ham'))
    sys.exit(1)

