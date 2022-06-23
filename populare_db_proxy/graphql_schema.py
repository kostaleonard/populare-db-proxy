"""Contains the GraphQL schema for API calls.

See the guide here for more information:
https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/
"""

from __future__ import annotations
from datetime import datetime
from graphene import ObjectType, String, Int, DateTime, Schema


class Query(ObjectType):
    """Represents available GraphQL queries."""

    read_posts = String(
        limit=Int(required=False),
        before=DateTime(required=False)
    )

    def resolve_read_posts(
            self,
            info,
            limit: int | None,
            before: datetime | None
    ) -> str:
        """Returns the response to a read_posts query.

        :param info: The GraphQL context.
        :param limit: The maximum number of posts to return from the database.
        :param before: If supplied, return posts created earlier than this
            date; if None, return the most recent posts (`before` is set to
            datetime.now()).
        """
        # TODO fix docstring
        # TODO why is the first arg in the guide not self--should this be static?
        # TODO what are the types of the root and info args?


def get_schema() -> Schema:
    """Returns the GraphQL schema for the proxy.

    :return: The GraphQL schema for the proxy.
    """
    return Schema(query=Query)
