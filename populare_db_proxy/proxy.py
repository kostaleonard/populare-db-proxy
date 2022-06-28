"""Contains the proxy server."""

from flask import Flask
from flask_graphql import GraphQLView
from populare_db_proxy.graphql_schema import get_schema
from populare_db_proxy.app_data import app


def create_app(flask_app: Flask) -> None:
    """Adds endpoints to the given flask app.

    :param flask_app: The app to which to add endpoints.
    """
    flask_app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
        'graphql',
        schema=get_schema(),
        graphiql=True,
    ))


def main() -> None:
    """Runs the program."""
    create_app(app)
    app.run()


if __name__ == "__main__":
    main()
