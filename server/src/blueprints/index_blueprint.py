from flask import Blueprint, render_template

from src.db import PostgresDatabase

from src.utils import Property

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/', methods=['GET'])
def render_properties():
    db = PostgresDatabase()
    db.connect()
    properties = db.get_properties()
    db.close()
    print(properties)
    return render_template('index.html', properties=[Property(*p) for p in properties])
