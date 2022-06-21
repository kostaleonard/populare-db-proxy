"""Tests rds.py."""

from datetime import datetime
import pytest
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError, IntegrityError
from populare_db_proxy.db_schema import Post
from populare_db_proxy.rds import init_db_schema, create_post, read_posts
from tests.conftest import DB_NAME


def test_rds_creation(mocked_rds: dict) -> None:
    """Tests that the mocked RDS was created successfully.

    :param mocked_rds: The mocked database JSON object.
    """
    assert mocked_rds["DBInstance"]["DBName"] == DB_NAME


def test_local_db_creation(populated_local_db: Engine) -> None:
    """Tests that the local database was created successfully.

    :param populated_local_db: A connection to the local, in-memory database.
    """
    with Session(populated_local_db) as session:
        with session.begin():
            statement = select(Post)
            results = session.execute(statement)
            assert list(results)


def test_init_db_schema_creates_tables(
        uninitialized_local_db: Engine
) -> None:
    """Tests that init_db_schema creates tables in the database.

    :param uninitialized_local_db: A connection to the local, in-memory
        database.
    """
    post = Post(text="text", author="author", created_at=datetime.now())
    with pytest.raises(OperationalError):
        # Because there are no tables, inserting raises an error.
        create_post(uninitialized_local_db, post)
    init_db_schema(uninitialized_local_db)
    create_post(uninitialized_local_db, post)
    assert post.id


def test_init_db_schema_twice_no_error(
        uninitialized_local_db: Engine
) -> None:
    """Tests that init_db_schema can be called twice without causing errors.

    :param uninitialized_local_db: A connection to the local, in-memory
        database.
    """
    post = Post(text="text", author="author", created_at=datetime.now())
    init_db_schema(uninitialized_local_db)
    init_db_schema(uninitialized_local_db)
    create_post(uninitialized_local_db, post)
    assert post.id


def test_create_post_adds_to_table(empty_local_db: Engine) -> None:
    """Tests that create_post adds posts to the database table.

    :param empty_local_db: A connection to the local, in-memory database.
    """
    post = Post(text="text", author="author", created_at=datetime.now())
    assert not read_posts(empty_local_db)
    create_post(empty_local_db, post)
    posts = read_posts(empty_local_db)
    assert len(posts) == 1
    assert posts[0].id == post.id


def test_create_post_adds_post_id(empty_local_db: Engine) -> None:
    """Tests that create_post adds an ID field to posts.

    :param empty_local_db: A connection to the local, in-memory database.
    """
    post = Post(text="text", author="author", created_at=datetime.now())
    assert not post.id
    create_post(empty_local_db, post)
    assert post.id


def test_create_post_return_value_matches_input(
        empty_local_db: Engine
) -> None:
    """Tests that create_post's return value is the same object as the input.

    :param empty_local_db: A connection to the local, in-memory database.
    """
    post = Post(text="text", author="author", created_at=datetime.now())
    returned_post = create_post(empty_local_db, post)
    assert post is returned_post


def test_create_post_twice_same_object_adds_once(
        empty_local_db: Engine
) -> None:
    """Tests that create_post will only add the same post object once when
    called twice.

    :param empty_local_db: A connection to the local, in-memory database.
    """
    post = Post(text="text", author="author", created_at=datetime.now())
    create_post(empty_local_db, post)
    create_post(empty_local_db, post)
    posts = read_posts(empty_local_db)
    assert len(posts) == 1


def test_create_post_twice_different_objects_same_content_adds_twice(
        empty_local_db: Engine
) -> None:
    """Tests that create_post adds different objects with the same content
    twice.

    :param empty_local_db: A connection to the local, in-memory database.
    """
    now = datetime.now()
    post1 = Post(text="text", author="author", created_at=now)
    post2 = Post(text="text", author="author", created_at=now)
    create_post(empty_local_db, post1)
    create_post(empty_local_db, post2)
    posts = read_posts(empty_local_db)
    assert len(posts) == 2


def test_create_post_auto_increment_id(empty_local_db: Engine) -> None:
    """Tests that create_post auto-increments IDs.

    :param empty_local_db: A connection to the local, in-memory database.
    """
    post1 = Post(text="text", author="author", created_at=datetime.now())
    post2 = Post(text="text", author="author", created_at=datetime.now())
    create_post(empty_local_db, post1)
    create_post(empty_local_db, post2)
    assert post1.id == 1
    assert post2.id == 2


def test_create_post_explicit_id(empty_local_db: Engine) -> None:
    """Tests that create_post accepts explicit post IDs.

    :param empty_local_db: A connection to the local, in-memory database.
    """
    post1 = Post(
        text="text",
        author="author",
        created_at=datetime.now(),
        id=10
    )
    post2 = Post(
        text="text",
        author="author",
        created_at=datetime.now(),
        id=20
    )
    create_post(empty_local_db, post1)
    create_post(empty_local_db, post2)
    assert post1.id == 10
    assert post2.id == 20


def test_create_post_id_collision_raises_error(empty_local_db: Engine) -> None:
    """Tests that create_post raises an error on ID collision.

    :param empty_local_db: A connection to the local, in-memory database.
    """
    post1 = Post(text="text", author="author", created_at=datetime.now(), id=1)
    post2 = Post(text="text", author="author", created_at=datetime.now(), id=1)
    create_post(empty_local_db, post1)
    with pytest.raises(IntegrityError):
        create_post(empty_local_db, post2)


def test_read_posts_returns_posts(populated_local_db: Engine) -> None:
    """Tests that read_posts returns a list of posts.

    :param populated_local_db: A connection to the local, in-memory database.
    """
    assert read_posts(populated_local_db)


def test_read_posts_observes_limit(populated_local_db: Engine) -> None:
    """Tests that read_posts observes the limit argument.

    :param populated_local_db: A connection to the local, in-memory database.
    """
    limit = 3
    posts = read_posts(populated_local_db, limit=limit)
    assert len(posts) == limit


def test_read_posts_sorts_output(empty_local_db: Engine) -> None:
    """Tests that read_posts orders the output chronologically.

    :param empty_local_db: A connection to the local, in-memory database.
    """
    # Create the posts in chronological order.
    post1 = Post(text="first", author="author", created_at=datetime.now())
    post2 = Post(text="second", author="author", created_at=datetime.now())
    post3 = Post(text="third", author="author", created_at=datetime.now())
    post4 = Post(text="fourth", author="author", created_at=datetime.now())
    # Add the posts in arbitrary order.
    create_post(empty_local_db, post2)
    create_post(empty_local_db, post4)
    create_post(empty_local_db, post3)
    create_post(empty_local_db, post1)
    # Returned posts should be in chronological order again.
    posts = read_posts(empty_local_db)
    assert posts[0].text == "fourth"
    assert posts[1].text == "third"
    assert posts[2].text == "second"
    assert posts[3].text == "first"


def test_read_posts_with_limit_has_most_recent_posts(
        empty_local_db: Engine
) -> None:
    """Tests that read_posts returns the most recent posts when a limit is
    used.

    :param empty_local_db: A connection to the local, in-memory database.
    """
    # Create the posts in chronological order.
    post1 = Post(text="first", author="author", created_at=datetime.now())
    post2 = Post(text="second", author="author", created_at=datetime.now())
    post3 = Post(text="third", author="author", created_at=datetime.now())
    post4 = Post(text="fourth", author="author", created_at=datetime.now())
    # Add the posts in arbitrary order.
    create_post(empty_local_db, post2)
    create_post(empty_local_db, post4)
    create_post(empty_local_db, post3)
    create_post(empty_local_db, post1)
    # Returned posts should be in chronological order again.
    limit = 3
    posts = read_posts(empty_local_db, limit=limit)
    assert len(posts) == limit
    assert posts[0].text == "fourth"
    assert posts[1].text == "third"
    assert posts[2].text == "second"


def test_read_posts_before_datetime(empty_local_db: Engine) -> None:
    """Tests that read_posts returns posts before an explicit datetime.

    :param empty_local_db: A connection to the local, in-memory database.
    """
    for idx in range(1, 5):
        post = Post(
            text=str(idx),
            author="author",
            created_at=datetime(2022, 1, idx)
        )
        create_post(empty_local_db, post)
    before = datetime(2022, 1, 3, hour=6)
    posts = read_posts(empty_local_db, before=before)
    assert len(posts) == 3
    assert posts[0].text == "3"
    assert posts[1].text == "2"
    assert posts[2].text == "1"
