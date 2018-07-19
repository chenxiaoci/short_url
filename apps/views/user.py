from flask import jsonify
from apps.libs.baseresource import BaseResource
from apps.validates.user import UserForm
from apps.models import User


class UserResource(BaseResource):
    """
    post: 注册
    get: 
    put: 
    """
    def post(self):
        form = UserForm().validate_for_api()
        user = User.save() 
        return jsonify(dict(user))


class DomainResource(BaseResource):
    pass


