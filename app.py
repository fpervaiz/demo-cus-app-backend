import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

basedir = os.path.abspath(os.path.dirname(__file__))

# Build the SQLite URL for SqlAlchemy
sqlite_url = "sqlite:///" + os.path.join(basedir, "data.db")

def basic_auth(username, password, required_scopes=None):
    if username == 'admin' and password == 'secret':
        return {'sub': 'admin'}

    # optional: raise exception for custom error response
    return None


if __name__ == '__main__':
    app = connexion.FlaskApp(__name__, specification_dir=basedir)
    app.add_api('swagger.yml')

    # Get the underlying Flask app instance
    app_instance = app.app

    # Configure the SqlAlchemy part of the app instance
    app_instance.config["SQLALCHEMY_ECHO"] = False
    app_instance.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
    app_instance.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Debug
    app_instance.url_map.strict_slashes = False
    CORS(app_instance)

    # Create the SqlAlchemy db instance
    db = SQLAlchemy(app_instance)

    # Initialize Marshmallow
    ma = Marshmallow(app_instance)

    app.run(port=5000)
    #app.run(port=5000, ssl_context='adhoc')