from flask import request, json
from werkzeug.exceptions import HTTPException


class ApiException(HTTPException):
    code = 500
    msg = 'sorry, we make a mistake'
    error_code = 999

    def __init__(self, code=None, msg=None, error_code=None, header=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        if error_code:
            self.error_code = error_code
        super(ApiException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            # 形如request="POST v1/client/register"
            request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        full_url = str(request.full_path)
        main_path = full_url.split('?')
        return main_path[0]



class DumplicatedStupid(ApiException):
    code = 400
    error_code = 2001
    msg = 'you are already a stypid'


class AuthFailed(ApiException):
    code = 401
    msg = 'authorization failed'
    error_code = 1005


class NotFound(ApiException):
    code = 404
    msg = 'the resource is not found 0.0 '
    error_code = 1001

class MethodNotAllowed(ApiException):
    code = 405
    msg = 'MethodNotAllowed,'
    error_code = 1006

