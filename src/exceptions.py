from rest_framework.exceptions import APIException


class ProtrendException(APIException):

    def __init__(self, detail=None, code=None, status=None):
        super(ProtrendException, self).__init__(detail=detail, code=code)

        if status is None:
            status = self.status_code

        self._status = status

    @property
    def status(self):
        return self._status

    @property
    def message(self):
        return self.get_full_details()
