"""Contains classes for the database schema."""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()
TEXT_SIZE = 255
AUTHOR_SIZE = 255


class Post(Base):
    """Defines the posts table."""

    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(TEXT_SIZE), nullable=False)
    author = Column(String(AUTHOR_SIZE), nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __repr__(self) -> str:
        """Returns the string representation of a row in the table.

        :return: The string representation of a row in the table.
        """
        return (
            f"Post(id={self.id!r}, text={self.text!r}, "
            f"author={self.author!r}, created_at={self.created_at!r})"
        )
