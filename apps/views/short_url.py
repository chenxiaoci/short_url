import ipdb
from apps.libs.baseresource import BaseResource

from flask import Blueprint, request, render_template, jsonify, redirect
from apps.models import Url
from apps.validates.url import UrlForm
urlbp = Blueprint('uri', __name__)

class UrlResource(BaseResource):
    """
    post: 提交长域名生成短域名
    """
    def post(self):
        form = UrlForm().validate_for_api()
        url = Url.save_url(form.long_url.data)
        return jsonify({'url': url.short_url}), 200

@urlbp.route('/<code>')
def redirect_to_long(code):
    long_url = Url.convert_to_long()
    return redirect(long_url, code=301)


@urlbp.route('/')
def index():
    return render_template('index.html')

