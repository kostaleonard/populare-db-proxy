"""Contains application configuration."""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics

_DATABASE_SECRET_PATH = "/etc/populare-db-proxy/db-certs/db-uri"


def get_database_uri(secret_filename: str = _DATABASE_SECRET_PATH) -> str:
    """Returns the database URI.

    The database URI is loaded from secret_filename, which is a
    Kubernetes secret volume mount. If the file is absent, this operation will
    raise a FileNotFoundError because it cannot correctly function in a
    distributed setting (see #19). However, for testing, the user can set the
    POPULARE_ALLOW_MISSING_SECRET environment variable, which will cause the
    database URI to be loaded from the SQLALCHEMY_DATABASE_URI environment
    variable, defaulting to the path /tmp/populare.db on the local filesystem.

    :param secret_filename: The path to the file containing the secret.
    :return: The database URI.
    """
    try:
        with open(secret_filename, "r", encoding="utf-8") as infile:
            return infile.read()
    except FileNotFoundError as exc:
        if "POPULARE_ALLOW_MISSING_SECRET" in os.environ:
            return os.environ.get(
                "SQLALCHEMY_DATABASE_URI",
                "sqlite:////tmp/populare.db"
            )
        raise exc


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
db = SQLAlchemy(app)
metrics = PrometheusMetrics(app)
