"""Contains functions for interfacing with AWS RDS.

See the AWS RDS Python interface documentation here:
https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.Connecting.Python.html
"""

from __future__ import annotations
from datetime import datetime
from sqlalchemy import select, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from populare_db_proxy.db_schema import Post, Base
from populare_db_proxy.app import db

READ_POSTS_LIMIT = 50


def init_db_schema() -> None:
    """Initializes the database schema."""
    db.create_all()


def create_post(engine: Engine, post: Post) -> Post:
    """Adds a post to the database.

    :param post: The post to add. The post need not have an explicitly set id
        field (i.e., it may be None). If None, post.id will be set by
        autoincrement; if set in advance, post.id will be kept, but this
        operation will raise an IntegrityError if there already exists a post
        in the database with that id. Therefore, we recommend that users do not
        supply an explicit id field.
    :return: The input post; post.id will be set if it was not before.
    """
    with Session(db.engine, expire_on_commit=False) as session:
        with session.begin():
            session.add(post)
    return post


def read_posts(
        limit: int = READ_POSTS_LIMIT,
        before: datetime | None = None
) -> list[Post]:
    """Returns a list of posts from the database.

    :param limit: The maximum number of posts to return from the database.
    :param before: If supplied, return posts created earlier than this date; if
        None, return the most recent posts (`before` is set to datetime.now()).
    :return: The no more than `limit` most recent posts created earlier than
        `before` (or now, if not supplied) in chronological order. The
        chronological order will be most recent first; index 0 will have the
        most recent post created earlier than `before`.
    """
    before = before if before else datetime.now()
    statement = (
        select(Post)
            .where(Post.created_at < before)
            .order_by(Post.created_at.desc())
            .limit(limit)
    )
    result = [row[0] for row in db.session.execute(statement)]
    return result
