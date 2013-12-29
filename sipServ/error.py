# core
import traceback


class SipError(Exception):
    def __init__(self, code, message, headers=[]):
        Exception.__init__(self, message)
        self.code = code
        self.headers = headers