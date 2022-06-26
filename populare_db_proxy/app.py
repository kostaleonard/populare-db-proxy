"""Contains application configuration."""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# TODO all of these should be secrets loaded into env
HOST = "sqlalchemytutorial.*****.eu-central1.rds.amazonaws.com"
DB_NAME = "populare_db"
ENGINE_URL = f"mysql+mysqlconnector://{'user'}:{'pass'}@{HOST}/{DB_NAME}"
ENGINE_URL_LOCAL = "sqlite+pysqlite:///:memory:"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "SQLALCHEMY_DATABASE_URI",
    "sqlite:////tmp/populare.db"
)
db = SQLAlchemy(app)
