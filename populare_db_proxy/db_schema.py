"""Contains classes for the database schema."""

from sqlalchemy.orm import declarative_base
from populare_db_proxy.app import db

Base = declarative_base()
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
        """Returns the string representation of a row in the table.

        :return: The string representation of a row in the table.
        """
        return (
            f"Post(id={self.id!r}, text={self.text!r}, "
            f"author={self.author!r}, created_at={self.created_at!r})"
        )
