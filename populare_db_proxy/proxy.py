"""Contains the proxy server."""

from flask_graphql import GraphQLView
from populare_db_proxy.graphql_schema import get_schema
from populare_db_proxy.app_data import app


def create_app() -> None:
    """TODO"""
    # TODO pure function
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
        'graphql',
        schema=get_schema(),
        graphiql=True,
    ))


def main() -> None:
    """Runs the program."""
    create_app()
    app.run()


if __name__ == "__main__":
    main()
