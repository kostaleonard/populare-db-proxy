"""Contains functions for interfacing with AWS RDS.

See the AWS RDS Python interface documentation here:
https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.Connecting.Python.html
"""

from __future__ import annotations
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from populare_db_proxy.db_schema import Base, Post

READ_POSTS_LIMIT = 50


def init_db_schema(engine: Engine) -> None:
    """Initializes the database schema.

    :param engine: The database engine.
    """
    Base.metadata.create_all(engine)


def create_post(engine: Engine, post: Post) -> Post:
    """TODO"""
    with Session(engine, expire_on_commit=False) as session:
        with session.begin():
            session.add(post)
    return post


def read_posts(engine: Engine, limit: int = READ_POSTS_LIMIT, start_at: datetime | None = None) -> list[Post]:
    """TODO read the most recent limit posts."""
