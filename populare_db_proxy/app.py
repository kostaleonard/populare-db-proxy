"""Contains application configuration."""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "SQLALCHEMY_DATABASE_URI",
    "sqlite:////tmp/populare.db"
)
db = SQLAlchemy(app)
