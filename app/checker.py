import re


class Checker(object):

    def is_spam(self, text):
        clean_text = self._clean_up_text(text)
        return (self._is_banned_words(clean_text) or
                self._is_link(clean_text) or
                self._is_phone_num(clean_text))

    def _is_phone_num(self, text):
        pattern = '\(?([0-9]{3,4})\)?[-.●]?([0-9]{3,4})[-.●]?([0-9]{3,4})'
        phone_num = re.search(pattern, text)
        if phone_num:
            print('Phone Num Detected')
        return phone_num

    def _is_link(self, text):
        pattern = '[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
        link = re.search(pattern, text)
        if link:
            print('Link detected')
        return link

    def _is_banned_words(self, text):
        pattern = '(jual|beli|www|thor)'
        banned_words = re.search(pattern, text)
        if banned_words:
            print('Banned words')
        return banned_words

    def _clean_up_text(self, text):
        pattern = '\W+'
        return re.sub(pattern, '', text).lower()

