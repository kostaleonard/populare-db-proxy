"""Contains the proxy server."""

from flask import Flask
from flask_graphql import GraphQLView


def main() -> None:
    """Runs the program."""
    app = Flask(__name__)
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
    ))
    app.run()


if __name__ == "__main__":
    main()
