"""Tests graphql_schema.py.

Tests the GraphQL schema directly, without using Flask; test_proxy.py contains
tests that issue POST requests on the graphql endpoint directly.
"""

from datetime import datetime
from populare_db_proxy.app_data import db
from populare_db_proxy.graphql_schema import get_schema


def test_resolve_init_returns_ok() -> None:
    """Tests that resolve_init_db returns ok."""
    db.drop_all()
    schema = get_schema()
    result = schema.execute("""
    {
        initDb
    }
    """)
    assert result.data["initDb"] == "ok"


def test_resolve_read_posts_no_db_fails() -> None:
    """Tests that resolve_read_posts fails when the database has not been
    initialized."""
    db.drop_all()
    schema = get_schema()
    result = schema.execute("""
    {
        readPosts
    }
    """)
    assert "no such table" in str(result.errors)


def test_resolve_read_posts_empty_db_returns_empty_list() -> None:
    """Tests that resolve_read_posts returns the empty list when the database
    is empty."""
    db.drop_all()
    schema = get_schema()
    _ = schema.execute("""
    {
        initDb
    }
    """)
    result = schema.execute("""
    {
        readPosts
    }
    """)
    assert result.data["readPosts"] == []


def test_resolve_create_post_returns_post_with_id() -> None:
    """Tests that resolve_read_posts returns the original post with ID."""
    db.drop_all()
    schema = get_schema()
    _ = schema.execute("""
    {
        initDb
    }
    """)
    result = schema.execute("""
    {
        createPost(
            text: "my text",
            author: "my author",
            createdAt: "2006-01-02T15:04:05"
        )
    }
    """)
    post_str = result.data["createPost"]
    assert "my text" in post_str
    assert "my author" in post_str
    assert "id" in post_str


def test_resolve_read_posts_returns_list_of_posts() -> None:
    """Tests that resolve_read_posts returns a list of posts."""
    db.drop_all()
    schema = get_schema()
    _ = schema.execute("""
    {
        initDb
    }
    """)
    for idx in range(5):
        _ = schema.execute(f"""
        {{
            createPost(
                text: "text{idx + 1}",
                author: "author{idx + 1}",
                createdAt: "{datetime.now().isoformat()}"
            )
        }}
        """)
    result = schema.execute("""
    {
        readPosts
    }
    """)
    posts = result.data["readPosts"]
    assert len(posts) == 5
    assert "text1" in posts[-1]
    assert "text5" in posts[0]


def test_resolve_update_post_returns_updated_post() -> None:
    """Tests that resolve_update_post returns the updated post."""
    db.drop_all()
    schema = get_schema()
    _ = schema.execute("""
    {
        initDb
    }
    """)
    for idx in range(5):
        _ = schema.execute(f"""
        {{
            createPost(
                text: "text{idx + 1}",
                author: "author{idx + 1}",
                createdAt: "{datetime.now().isoformat()}"
            )
        }}
        """)
    # Update the text field.
    result = schema.execute(f"""
    {{
        updatePost(
            postId: 1,
            text: "text_one",
            author: "author1",
            createdAt: "2006-01-02T15:04:05"
        )
    }}
    """)
    post = result.data["updatePost"]
    assert "text1" not in post
    assert "text_one" in post


def test_resolve_update_post_updates_post() -> None:
    """Tests that resolve_update_post updates the specified post."""
    db.drop_all()
    schema = get_schema()
    _ = schema.execute("""
    {
        initDb
    }
    """)
    for idx in range(5):
        _ = schema.execute(f"""
        {{
            createPost(
                text: "text{idx + 1}",
                author: "author{idx + 1}",
                createdAt: "{datetime.now().isoformat()}"
            )
        }}
        """)
    # Update the text field.
    _ = schema.execute(f"""
    {{
        updatePost(
            postId: 1,
            text: "text_one",
            author: "author1",
            createdAt: "2006-01-02T15:04:05"
        )
    }}
    """)
    result = schema.execute("""
    {
        readPosts
    }
    """)
    posts = result.data["readPosts"]
    assert "textone" not in posts[-1]
    assert "text_one" in posts[-1]


def test_resolve_delete_post_deletes_post() -> None:
    """Tests that resolve_delete_post deletes the specified post."""
    db.drop_all()
    schema = get_schema()
    _ = schema.execute("""
    {
        initDb
    }
    """)
    for idx in range(5):
        _ = schema.execute(f"""
        {{
            createPost(
                text: "text{idx + 1}",
                author: "author{idx + 1}",
                createdAt: "{datetime.now().isoformat()}"
            )
        }}
        """)
    _ = schema.execute("""
    {
        deletePost(
            postId: 1
        )
    }
    """)
    result = schema.execute("""
    {
        readPosts
    }
    """)
    posts = result.data["readPosts"]
    assert len(posts) == 4
    assert "text2" in posts[-1]
    assert "text5" in posts[0]
