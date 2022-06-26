"""Contains the GraphQL schema for API calls.

See the guide here for more information:
https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/
"""

from __future__ import annotations
from datetime import datetime
from sqlalchemy import create_engine, select
from graphene import ObjectType, String, Int, DateTime, Schema
from graphql.execution.base import ResolveInfo
from populare_db_proxy.rds import (
    init_db_schema,
    read_posts as db_read_posts,
    ENGINE_URL_LOCAL
)
from populare_db_proxy.db_schema import Post
from populare_db_proxy.app import db


class Query(ObjectType):
    """Represents available GraphQL queries."""

    init_db = String()
    read_posts = String(
        limit=Int(required=False),
        before=DateTime(required=False)
    )

    @staticmethod
    def resolve_init_db(root: ObjectType | None, info: ResolveInfo) -> str:
        """Initializes the database schema and returns the response.

        curl -d '{ initDb }' -H "Content-Type: application/graphql" -X POST
        http://localhost:5000/graphql

        :param root: The root GraphQL object.
        :param info: The GraphQL context.
        :return: The response to an init_db query.
        """

        db.create_all()
        '''
        post = Post(text="text", author="author", created_at=datetime.now())
        db.session.add(post)
        db.session.commit()
        print(Post.query.all())
        '''
        #init_db_schema(db.engine)
        return "ok"

    @staticmethod
    def resolve_read_posts(
            root: ObjectType | None,
            info: ResolveInfo,
            limit: int | None = None,
            before: datetime | None = None
    ) -> str:
        """Returns the response to a read_posts query.

        curl -d '{ readPosts }' -H "Content-Type: application/graphql" -X POST
        http://localhost:5000/graphql

        :param root: The root GraphQL object.
        :param info: The GraphQL context.
        :param limit: The maximum number of posts to return from the database.
            If not specified, uses the package default.
        :param before: If supplied, return posts created earlier than this
            date; if None, return the most recent posts (`before` is set to
            datetime.now()).
        :return: The response to a read_posts query.
        """
        
        before = before if before else datetime.now()
        statement = (
            select(Post)
                .where(Post.created_at < before)
                .order_by(Post.created_at.desc())
                .limit(limit)
        )
        result = [row[0] for row in db.session.execute(statement)]
        return str(result)

        #return str(db_read_posts(db.engine, limit=limit, before=before))


def get_schema() -> Schema:
    """Returns the GraphQL schema for the proxy.

    :return: The GraphQL schema for the proxy.
    """
    return Schema(query=Query)
