import os


def seconds_to_time(seconds):
    seconds = int(seconds)
    return '{hours:02d}:{minutes:02d}:{seconds:02d}'.format(hours=(seconds // 60), minutes=(seconds // 60 % 60), seconds=(seconds % 60))

def delete_file(file_path):
    os.remove(file_path)

