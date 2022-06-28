"""Contains classes for the database schema."""

import json
from populare_db_proxy.app_data import db

TEXT_SIZE = 255
AUTHOR_SIZE = 255


class Post(db.Model):
    """Defines the posts table."""
    # pylint: disable=too-few-public-methods

    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(TEXT_SIZE), nullable=False)
    author = db.Column(db.String(AUTHOR_SIZE), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self) -> str:
        """Returns the JSON serialization of a row in the table.

        :return: The JSON serialization of a row in the table.
        """
        fields = {
            "id": self.id,
            "text": self.text,
            "author": self.author,
            "created_at": self.created_at.isoformat()
        }
        return json.dumps(fields)
