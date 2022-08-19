"""Contains the proxy server."""

from flask import Flask
from flask_graphql import GraphQLView
from populare_db_proxy.graphql_schema import get_schema
from populare_db_proxy.app_data import app
from populare_db_proxy.db_ops import init_db_schema


@app.route("/health")
def health() -> str:
    """Returns the content of the health endpoint.

    :return: The content of the health endpoint.
    """
    return "ok"


def create_app() -> Flask:
    """Adds endpoints to the Flask app and returns it.

    :return: The Flask app.
    """
    init_db_schema()
    app.add_url_rule("/graphql", view_func=GraphQLView.as_view(
        "graphql",
        schema=get_schema(),
        graphiql=True,
    ))
    return app


def main() -> None:
    """Runs the program.

    This function is only called when the app is run as standalone Flask; it is
    not called when run as a Gunicorn WSGI, as in production deployment.
    """
    create_app()
    app.run()


if __name__ == "__main__":
    main()
