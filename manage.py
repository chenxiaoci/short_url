from flask_script import Manager
from flask_migrate import MigrateCommand
from apps import create_app

application = create_app()
manager = Manager(application)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    #application.run()
    manager.run()
