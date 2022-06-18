"""Contains functions for interfacing with AWS RDS.

See the AWS RDS Python interface documentation here:
https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.Connecting.Python.html
"""

RECENT_POSTS_LIMIT = 50


def get_recent_posts(limit: int = RECENT_POSTS_LIMIT) -> dict:
    """TODO"""
