import collections

Comment = collections.namedtuple('Comment', [
    'parent_id',
    'comment_id',
    'body',
    'created_utc',
    'score',
    'subreddit',
    'parent_data'
])
