from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from foodtruck import create_app, db

application = create_app(config_from_env='APP_SETTINGS')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()
