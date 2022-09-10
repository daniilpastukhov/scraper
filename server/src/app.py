import os

from flask import Flask

from src.blueprints.index_blueprint import index_blueprint


class AppWrapper:
    def __init__(self):
        self._app = Flask(__name__, template_folder='/app/templates')
        self.register_blueprints()

    def run(self):
        self._app.run(host=os.getenv('FLASK_HOST'), port=os.getenv('FLASK_PORT'))

    def register_blueprints(self):
        self._app.register_blueprint(index_blueprint)

    @property
    def app(self):
        return self._app
