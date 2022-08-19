"""Tests db_ops.py."""

from datetime import datetime
from multiprocessing import Pool
import pytest
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError, IntegrityError
from populare_db_proxy.db_schema import Post
from populare_db_proxy.db_ops import (
    init_db_schema,
    create_post,
    read_posts,
    update_post,
    delete_post
)
from tests.conftest import DB_NAME

POOL_SIZE = 10
NUM_PARALLEL_POSTS = 1000


def test_rds_creation(mocked_rds: dict) -> None:
    """Tests that the mocked RDS was created successfully.

    :param mocked_rds: The mocked database JSON object.
    """
    assert mocked_rds["DBInstance"]["DBName"] == DB_NAME


def test_local_db_creation(populated_local_db: Engine) -> None:
    """Tests that the local database was created successfully.

    :param populated_local_db: A connection to the local database.
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

    :param uninitialized_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    post = Post(text="text", author="author", created_at=datetime.now())
    with pytest.raises(OperationalError):
        # Because there are no tables, inserting raises an error.
        create_post(post)
    init_db_schema()
    create_post(post)
    assert post.id


def test_init_db_schema_twice_no_error(
        uninitialized_local_db: Engine
) -> None:
    """Tests that init_db_schema can be called twice without causing errors.

    :param uninitialized_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    post = Post(text="text", author="author", created_at=datetime.now())
    init_db_schema()
    init_db_schema()
    create_post(post)
    assert post.id


def test_create_post_adds_to_table(empty_local_db: Engine) -> None:
    """Tests that create_post adds posts to the database table.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    post = Post(text="text", author="author", created_at=datetime.now())
    assert not read_posts()
    create_post(post)
    posts = read_posts()
    assert len(posts) == 1
    assert posts[0].id == post.id


def test_create_post_adds_post_id(empty_local_db: Engine) -> None:
    """Tests that create_post adds an ID field to posts.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    post = Post(text="text", author="author", created_at=datetime.now())
    assert not post.id
    create_post(post)
    assert post.id


def test_create_post_return_value_matches_input(
        empty_local_db: Engine
) -> None:
    """Tests that create_post's return value is the same object as the input.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    post = Post(text="text", author="author", created_at=datetime.now())
    returned_post = create_post(post)
    assert post is returned_post


def test_create_post_twice_same_object_adds_once(
        empty_local_db: Engine
) -> None:
    """Tests that create_post will only add the same post object once when
    called twice.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    post = Post(text="text", author="author", created_at=datetime.now())
    create_post(post)
    create_post(post)
    posts = read_posts()
    assert len(posts) == 1


def test_create_post_twice_different_objects_same_content_adds_twice(
        empty_local_db: Engine
) -> None:
    """Tests that create_post adds different objects with the same content
    twice.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    now = datetime.now()
    post1 = Post(text="text", author="author", created_at=now)
    post2 = Post(text="text", author="author", created_at=now)
    create_post(post1)
    create_post(post2)
    posts = read_posts()
    assert len(posts) == 2


def test_create_post_auto_increment_id(empty_local_db: Engine) -> None:
    """Tests that create_post auto-increments IDs.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    post1 = Post(text="text", author="author", created_at=datetime.now())
    post2 = Post(text="text", author="author", created_at=datetime.now())
    create_post(post1)
    create_post(post2)
    assert post1.id == 1
    assert post2.id == 2


def test_create_post_explicit_id(empty_local_db: Engine) -> None:
    """Tests that create_post accepts explicit post IDs.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
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
    create_post(post1)
    create_post(post2)
    assert post1.id == 10
    assert post2.id == 20


def test_create_post_id_collision_raises_error(empty_local_db: Engine) -> None:
    """Tests that create_post raises an error on ID collision.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    post1 = Post(text="text", author="author", created_at=datetime.now(), id=1)
    post2 = Post(text="text", author="author", created_at=datetime.now(), id=1)
    create_post(post1)
    with pytest.raises(IntegrityError):
        create_post(post2)


def test_read_posts_returns_posts(populated_local_db: Engine) -> None:
    """Tests that read_posts returns a list of posts.

    :param populated_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    assert read_posts()


def test_read_posts_observes_limit(populated_local_db: Engine) -> None:
    """Tests that read_posts observes the limit argument.

    :param populated_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    limit = 3
    posts = read_posts(limit=limit)
    assert len(posts) == limit


def test_read_posts_sorts_output(empty_local_db: Engine) -> None:
    """Tests that read_posts orders the output chronologically.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    # Create the posts in chronological order.
    post1 = Post(text="first", author="author", created_at=datetime.now())
    post2 = Post(text="second", author="author", created_at=datetime.now())
    post3 = Post(text="third", author="author", created_at=datetime.now())
    post4 = Post(text="fourth", author="author", created_at=datetime.now())
    # Add the posts in arbitrary order.
    create_post(post2)
    create_post(post4)
    create_post(post3)
    create_post(post1)
    # Returned posts should be in chronological order again.
    posts = read_posts()
    assert posts[0].text == "fourth"
    assert posts[1].text == "third"
    assert posts[2].text == "second"
    assert posts[3].text == "first"


def test_read_posts_with_limit_has_most_recent_posts(
        empty_local_db: Engine
) -> None:
    """Tests that read_posts returns the most recent posts when a limit is
    used.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    # Create the posts in chronological order.
    post1 = Post(text="first", author="author", created_at=datetime.now())
    post2 = Post(text="second", author="author", created_at=datetime.now())
    post3 = Post(text="third", author="author", created_at=datetime.now())
    post4 = Post(text="fourth", author="author", created_at=datetime.now())
    # Add the posts in arbitrary order.
    create_post(post2)
    create_post(post4)
    create_post(post3)
    create_post(post1)
    # Returned posts should be in chronological order again.
    limit = 3
    posts = read_posts(limit=limit)
    assert len(posts) == limit
    assert posts[0].text == "fourth"
    assert posts[1].text == "third"
    assert posts[2].text == "second"


def test_read_posts_before_datetime(empty_local_db: Engine) -> None:
    """Tests that read_posts returns posts before an explicit datetime.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    for idx in range(1, 5):
        post = Post(
            text=str(idx),
            author="author",
            created_at=datetime(2022, 1, idx)
        )
        create_post(post)
    before = datetime(2022, 1, 3, hour=6)
    posts = read_posts(before=before)
    assert len(posts) == 3
    assert posts[0].text == "3"
    assert posts[1].text == "2"
    assert posts[2].text == "1"


def _parallel_create_post(idx: int) -> None:
    """Creates a sample post; for use in parallel processing.

    :param idx: The worker index; unused.
    """
    # pylint: disable=unused-argument
    post = Post(text="text", author="author", created_at=datetime.now())
    create_post(post)


@pytest.mark.xfail
def test_parallel_writes_no_race_condition(empty_local_db: Engine) -> None:
    """Tests that many create_post calls can run in parallel without any
    integrity violations.

    This test may occasionally fail if one of the processes cannot get a lock
    on the database. Failure happens only rarely and does not represent a
    breach of database integrity, so we allow this test to fail. See #32 for
    more information.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    with Pool(POOL_SIZE) as pool:
        pool.map(_parallel_create_post, range(NUM_PARALLEL_POSTS))
    # This number could be anything >= 1.
    num_erroneous_additions = 10
    posts = read_posts(limit=NUM_PARALLEL_POSTS + num_erroneous_additions)
    assert len(posts) == NUM_PARALLEL_POSTS
    assert (
            set(post.id for post in posts) ==
            set(range(1, NUM_PARALLEL_POSTS + 1))
    )


def test_update_post_returns_post(empty_local_db: Engine) -> None:
    """Tests that update_post returns the input post.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    post = Post(text="text", author="author", created_at=datetime.now())
    create_post(post)
    post = Post(
        text="new",
        author="new",
        created_at=datetime.now(),
        id=post.id
    )
    updated_post = update_post(post)
    assert updated_post.id == post.id
    assert updated_post.text == post.text
    assert updated_post.author == post.author
    assert updated_post.created_at == post.created_at


def test_update_post_changes_content(empty_local_db: Engine) -> None:
    """Tests that update_post changes post content.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    post = Post(text="text", author="author", created_at=datetime.now())
    create_post(post)
    post = Post(
        text="new",
        author="new",
        created_at=datetime.now(),
        id=post.id
    )
    update_post(post)
    posts = read_posts()
    assert len(posts) == 1
    assert posts[0].id == post.id
    assert posts[0].text == "new"
    assert posts[0].author == "new"


def test_update_post_invalid_id_no_error(empty_local_db: Engine) -> None:
    """Tests that update_post does not raise an error when the ID does not
    exist.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    invalid_id = 9
    post = Post(
        text="new",
        author="new",
        created_at=datetime.now(),
        id=invalid_id
    )
    _ = update_post(post)
    assert True


def test_update_post_date_changes_read_order(empty_local_db: Engine) -> None:
    """Tests that update_post with a new date changes the sort order in
    read_posts.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    # Create the posts in chronological order.
    post1 = Post(text="first", author="author", created_at=datetime.now())
    post2 = Post(text="second", author="author", created_at=datetime.now())
    post3 = Post(text="third", author="author", created_at=datetime.now())
    post4 = Post(text="fourth", author="author", created_at=datetime.now())
    # Add the posts in arbitrary order.
    create_post(post2)
    create_post(post4)
    create_post(post3)
    create_post(post1)
    # Update dates.
    post1 = Post(
        text="first",
        author="author",
        created_at=datetime.now(),
        id=post1.id
    )
    update_post(post1)
    # Post order should change.
    posts = read_posts()
    assert len(posts) == 4
    assert posts[0].text == "first"
    assert posts[1].text == "fourth"
    assert posts[2].text == "third"
    assert posts[3].text == "second"


def test_delete_post_removes_post(empty_local_db: Engine) -> None:
    """Tests that delete_post removes a post from the database.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    post1 = Post(text="first", author="author", created_at=datetime.now())
    post2 = Post(text="second", author="author", created_at=datetime.now())
    create_post(post1)
    create_post(post2)
    delete_post(post1.id)
    posts = read_posts()
    assert len(posts) == 1
    assert posts[0].text == "second"


def test_delete_post_invalid_id_no_error(empty_local_db: Engine) -> None:
    """Tests that delete_post does not raise an error when the ID does not
    exist.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    invalid_id = 9
    delete_post(invalid_id)
    assert True


def test_sequential_crud_method_calls(empty_local_db: Engine) -> None:
    """Tests that create, read, update, and delete can be called several times
    in arbitrary order.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    post1 = Post(text="first", author="author", created_at=datetime.now())
    post2 = Post(text="second", author="author", created_at=datetime.now())
    post3 = Post(text="third", author="author", created_at=datetime.now())
    post4 = Post(text="fourth", author="author", created_at=datetime.now())
    # Add the posts in arbitrary order.
    create_post(post2)
    create_post(post4)
    create_post(post3)
    create_post(post1)
    # Update date.
    post1 = Post(
        text="first",
        author="author",
        created_at=datetime.now(),
        id=post1.id
    )
    update_post(post1)
    # Delete some posts.
    delete_post(post2.id)
    delete_post(post3.id)
    # Read posts.
    posts = read_posts()
    assert len(posts) == 2
    # Add more posts.
    post5 = Post(text="fifth", author="author", created_at=datetime.now())
    post6 = Post(text="sixth", author="author", created_at=datetime.now())
    create_post(post5)
    create_post(post6)
    # Update date.
    post6 = Post(
        text="sixth",
        author="author",
        created_at=datetime.now(),
        id=post6.id
    )
    update_post(post6)
    # Read posts again.
    posts = read_posts()
    assert len(posts) == 4


def test_read_posts_recovers_after_error(
        uninitialized_local_db: Engine
) -> None:
    """Tests that read_posts still functions correctly after an error.

    :param uninitialized_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    with pytest.raises(OperationalError):
        # Because there are no tables, reading raises an error.
        _ = read_posts()
    init_db_schema()
    posts = read_posts()
    assert posts is not None
