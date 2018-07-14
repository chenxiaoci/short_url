from flask_sqlalchemy import SQLAlchemy
#from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
# from apps.views import create_blueprint
db = SQLAlchemy()
migrate = Migrate(db=db)
#bootstrap = Bootstrap()

def create_ext(app):
    migrate.init_app(app) 
    #bootstrap.init_app(app)
    db.init_app(app) 
