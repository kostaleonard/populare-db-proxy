"""Contains the proxy server."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_graphql import GraphQLView
from sqlalchemy.engine import create_engine
from populare_db_proxy.graphql_schema import get_schema
from populare_db_proxy.rds import ENGINE_URL_LOCAL
from populare_db_proxy.app import db, app


def main() -> None:
    """Runs the program."""
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
        'graphql',
        schema=get_schema(),
        graphiql=True,
    ))
    app.run()


if __name__ == "__main__":
    main()
