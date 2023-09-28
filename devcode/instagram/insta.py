from instapy import InstaPy
from instapy.util import smart_run

session = InstaPy(username="", password="")

with smart_run(session, threaded=True):
    session.like_by_tags(tags=['photography','landscape'], amount=5)

    session.follow_by_tags(['tag1', 'tag2'], amount=10)

    session.follow_by_list(followlist=['samantha3', 'larry_ok'], times=1, sleep_delay=600, interact=False)

    session.follow_user_followers(['friend1', 'friend2', 'friend3'], amount=10, randomize=False, interact=True)

    # find more functions here: https://github.com/InstaPy/InstaPy/blob/master/docs/actions.md
