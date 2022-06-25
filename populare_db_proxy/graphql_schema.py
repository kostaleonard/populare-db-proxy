"""Contains the GraphQL schema for API calls.

See the guide here for more information:
https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/
"""

from __future__ import annotations
from datetime import datetime
from sqlalchemy import create_engine
from graphene import ObjectType, String, Int, DateTime, Schema
from graphql.execution.base import ResolveInfo
from populare_db_proxy.rds import (
    init_db_schema,
    read_posts as db_read_posts,
    ENGINE_URL_LOCAL
)
ENGINE = create_engine(ENGINE_URL_LOCAL).connect()


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
        init_db_schema(ENGINE)
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
        return str(db_read_posts(ENGINE, limit=limit, before=before))


def get_schema() -> Schema:
    """Returns the GraphQL schema for the proxy.

    :return: The GraphQL schema for the proxy.
    """
    return Schema(query=Query)
