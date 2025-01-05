from instagrapi import Client
import os
from dotenv import load_dotenv
load_dotenv()

INSTA_LOGIN = os.getenv('INSTA_LOGIN')
INSTA_PASS = os.getenv('INSTA_PASS')


cl = Client()
cl.login(INSTA_LOGIN, INSTA_PASS)

following = cl.user_following(cl.user_id)
print(following)
# for user_id in followers.keys():
#     cl.user_unfollow(user_id)
# follow_by_username
# unfollow_by_username
# get_followers
# get_followers_usernames
# get_following