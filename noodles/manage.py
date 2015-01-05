import logging
from flask.ext.script import Manager
#from flask.ext.assets import ManageAssets

from noodles.views import app


log = logging.getLogger(__name__)
manager = Manager(app)
# manager.add_command("assets", ManageAssets(assets))


@manager.command
def index():
    pass

if __name__ == "__main__":
    manager.run()
