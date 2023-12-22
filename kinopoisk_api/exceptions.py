class KinopoiskException(Exception):
    pass


class BadRequest(KinopoiskException):
    def __init__(self, request):
        self.request = request

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self}')"
