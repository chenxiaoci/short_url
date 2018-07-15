import re
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from apps.validates.base import BaseForm
from apps.models import User 


class UserForm(BaseForm):
    nickname = StringField('用户名', validators=[DataRequired('用户名不可以为空')])
    password = PasswordField('密码', validators=[DataRequired('密码不可以为空'), Length(3, 16), EqualTo('confirm', message='两次输入的密码不一致')])
    confirm = PasswordField('密码', validators=[DataRequired('密码不可以为空'), Length(3, 16)])
    email = StringField(validators=[Email(message='邮箱不可以为空')])

    def validate_nickname(self, value):
        user = User.query.filter_by(nick_name=value.data).first()
        if user:
            raise ValidationError(message='重复的用户名')

    def validate_email(self, value):
        user = User.query.filter_by(email=value.data).first()
        if user:
            raise ValidationError(message='重复的邮箱')
