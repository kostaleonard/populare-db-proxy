"""Contains the GraphQL schema for API calls.

See the guide here for more information:
https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/
"""

from __future__ import annotations
from datetime import datetime
from graphene import (
    ObjectType,
    String,
    Int,
    DateTime,
    Schema,
    ResolveInfo,
    List
)
from populare_db_proxy.rds import (
    read_posts as db_read_posts,
    init_db_schema,
    create_post as db_create_post
)
from populare_db_proxy.db_schema import Post


class Query(ObjectType):
    """Represents available GraphQL queries."""

    init_db = String()
    read_posts = List(
        String,
        limit=Int(required=False),
        before=DateTime(required=False)
    )
    create_post = String(
        text=String(),
        author=String(),
        created_at=DateTime()
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
        # pylint: disable=unused-argument
        init_db_schema()
        return "ok"

    @staticmethod
    def resolve_read_posts(
            root: ObjectType | None,
            info: ResolveInfo,
            limit: int | None = None,
            before: datetime | None = None
    ) -> list[str]:
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
        # pylint: disable=unused-argument
        # TODO do we want to return list[Post]? Can we?
        return [
            str(post) for post in db_read_posts(limit=limit, before=before)
        ]

    @staticmethod
    def resolve_create_post(
            root: ObjectType | None,
            info: ResolveInfo,
            text: str,
            author: str,
            created_at: datetime
    ) -> str:
        """Returns the response to a create_post query.

        createPost(text: "my text", author: "my author", createdAt:
        "2006-01-02T15:04:05") }' -H "Content-Type: application/graphql" -X
        POST http://localhost:5000/graphql

        :param root: The root GraphQL object.
        :param info: The GraphQL context.
        :param text: The text of the post.
        :param author: The author of the post.
        :param created_at: The datetime at which the post was created. For
            POST requests, format this as an ISO string.
        :return: The response to a create_post query.
        """
        # pylint: disable=unused-argument
        post = Post(text=text, author=author, created_at=created_at)
        db_create_post(post)
        return str(post)


def get_schema() -> Schema:
    """Returns the GraphQL schema for the proxy.

    :return: The GraphQL schema for the proxy.
    """
    return Schema(query=Query)
