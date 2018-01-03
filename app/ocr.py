import os

import pytesseract
import cv2
from PIL import Image

from app.utils import delete_file


class OCR(object):

    def __init__(self, image_location):
        self.image_location = image_location

    def to_text(self):
        image = cv2.imread(self.image_location)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        file_location = '{}.png'.format(os.getpid())
        cv2.imwrite(file_location, gray)

        text = pytesseract.image_to_string(Image.open(file_location))
        delete_file(file_location)
        print(text)

        cv2.imshow('Image', image)
        cv2.imshow('Output', gray)
        cv2.waitKey(0)
        return text

