"""Contains functions for interfacing with the database, including AWS RDS.

See the AWS RDS Python interface documentation here:
https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.Connecting.Python.html
"""

from __future__ import annotations
from datetime import datetime
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from populare_db_proxy.db_schema import Post
from populare_db_proxy.app_data import db

READ_POSTS_LIMIT = 50


def init_db_schema() -> None:
    """Initializes the database schema."""
    try:
        db.create_all()
    except OperationalError:
        # If the database already exists, this operation sometimes (not always)
        # raises an error.
        pass


def create_post(post: Post) -> Post:
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
    with Session(db.engine, expire_on_commit=False) as session:
        with session.begin():
            rows = session.execute(statement)
            result = [row[0] for row in rows]
    return result


def update_post(post: Post) -> Post:
    """Updates a post in the database.

    :param post: The post to update. The post's id field should be set to the
        post that the user wants to update in the database; all other fields
        should be set to the values that the caller would like the updated post
        to have. If no post exists in the database with the specified id,
        this operation does not raise an error, since that is the behavior of
        SQL.
    :return: The input post; the post with the corresponding id in the database
        will be updated to match the input.
    """
    statement = (
        update(Post)
            .where(Post.id == post.id)
            .values(
                text=post.text,
                author=post.author,
                created_at=post.created_at
            )
    )
    with Session(db.engine, expire_on_commit=False) as session:
        with session.begin():
            session.execute(statement)
    return post


def delete_post(post_id: int) -> None:
    """Deletes a post in the database.

    :param post_id: The id of the post to delete. If no post exists in the
        database with the specified id, this operation does not raise an error,
        since that is the behavior of SQL.
    """
    statement = delete(Post).where(Post.id == post_id)
    with Session(db.engine, expire_on_commit=False) as session:
        with session.begin():
            session.execute(statement)
