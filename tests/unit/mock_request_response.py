class MockRequestResponse:
    """
    Class created to mock a request Response. Used for tests including a request response.
    """

    _json = None
    _text = None
    status_code = None

    def __init__(self, text: str, json: dict = {}, satus_code: int = 200):
        self._text = text
        self._json = json
        self.satus_code = satus_code

    def json(self):
        return self._json

    def text(self):
        return self._text
