from datetime import datetime
import uuid
from flask import current_app, request
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,  BadSignature, SignatureExpired
from apps.ext import db
from apps.libs.code import generic_codes
from apps.libs.error import ApiException, DumplicatedStupid, AuthFailed, NotFound



class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_url_code = db.Column(db.String(32))
    long_url = db.Column(db.String(1000))
    create_time = db.Column(db.DateTime(), default=datetime.now)

    @classmethod
    def is_unique_short_url(cls, value=None):
        """ 传入code判断是否唯一"""
        urls = cls.query.filter_by(short_url_code=value).first()
        if urls:
            return False
        else:
            return True

    @property
    def short_url(self):
        """短域名"""
        return current_app.config['BASE_URL'] + self.short_url_code

    @classmethod
    def generic_short_url_code(cls):
        short_url_code = generic_codes(5)
        return short_url_code if cls.is_unique_short_url(short_url_code) else generic_short_url_code(cls)
    
    @classmethod
    def save_url(cls, long_url):
        url = cls.has_the_long_url(long_url)
        if url:
            return url
        short_url_code = cls.generic_short_url_code() 
        url = cls(short_url_code=short_url_code, long_url=long_url)
        db.session.add(url)
        db.session.commit()
        return url

    @classmethod
    def has_the_long_url(cls, long_url):
        url = cls.query.filter_by(long_url=long_url).first()
        return url if url else None

    @classmethod
    def convert_to_long(cls):
        """短域名访问后需要转为常常的域名"""
        code = request.path.strip('/')
        url = cls.query.filter_by(short_url_code=code).first()
        if url:
            long_url = url.long_url
            if not long_url.startswith('http'):
                long_url = 'http://' + long_url 
            return long_url
        else:
            raise ApiException(msg='not found', code=404, error_code=404)
            


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _uuid = db.Column(db.String(64))
    nick_name = db.Column(db.String(20), default='未知')
    email = db.Column(db.String(30))
    _password = db.Column(db.String(128))
    confirm = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def keys(self):
        return ['id', 'email']

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def hide_email(self):
        mail = self.email
        return mail[:2] + '*'*3 + mail[-2]

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @property
    def uuid(self):
        return self._uuid

    def generic_uuid(self):
        public_id = str(uuid.uuid4())
        self._uuid = public_id

    def check_password(self, raw):
        result = check_password_hash(self._password, raw)
        if not result:
            raise AuthFailed()

    @classmethod
    def save(cls):
        try: 
            user = cls()
            user.nick_name = request.get_json().get('nickname')
            user.password = request.get_json().get('password')
            user.email= request.get_json().get('email')
            user.generic_uuid()
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ApiException()
        return user

    @classmethod
    def users_count(cls):
        """用户总数"""
        return cls.query.count()

    def generic_confirm_code(self):
        """生成用户邮箱验证链接后的字符串"""
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=6000)
        code = s.dumps({
            'id': self.id
        })
        return code.decode('ascii')

    @classmethod
    def verify_confirm_code(cls, raw):
        """验证用户邮箱链接"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(raw)
        except BadSignature as e:
            raise AuthFailed(msg='confirm_code is invalid', error_code=1002)
        except SignatureExpired as e:
            raise AuthFailed(msg='confirm_code is expired', error_code=1002)
        except Exception as e:
            raise e
        id = data.get('id')
        user = cls.query.filter_by(id=id).first()
        if not user:
            raise NotFound(msg='user is not found')
        return user

    def generic_token(self):
        """生成token"""
        if not self.confirm:
            raise AuthFailed(msg='未激活')
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        code = s.dumps({
            'id': self.id,
            'uuid': self.uuid
        })
        return code.decode('ascii')

