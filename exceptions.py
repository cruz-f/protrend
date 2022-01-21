from rest_framework.exceptions import APIException


class ProtrendException(APIException):

    @property
    def status(self):
        return self.status_code

    @property
    def error(self):
        return self.get_full_details()