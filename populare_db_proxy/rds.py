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
    """Initializes the database schema."""
    # TODO if it already exists, does this raise an error?
    Base.metadata.create_all(engine)


def create_post(engine: Engine, post: Post) -> Post:
    """TODO"""
    #post_table = Base.metadata.tables["posts"]
    #stmt = insert(user_table).values(text=text, author=author, created_at=created_at)
    #with ENGINE.begin() as conn:
    #    result = conn.execute(stmt)
    with Session(engine) as session:
        session.add(post)
        session.commit()
    # Post now has an ID.
    return post


def read_posts(engine: Engine, limit: int = READ_POSTS_LIMIT, start_at: datetime | None = None) -> list[Post]:
    """TODO read the most recent limit posts."""
