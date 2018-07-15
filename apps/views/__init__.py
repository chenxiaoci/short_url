from .short_url import urlbp, UrlResource
from .user import UserResource


def create_blueprint(app):
    app.register_blueprint(urlbp)
    app.add_url_rule('/api/short', view_func=UrlResource.as_view('short'))
    app.add_url_rule('/api/user', view_func=UserResource.as_view('user'))
