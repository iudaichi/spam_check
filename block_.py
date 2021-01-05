
import tweepy
import os
import datetime


def judge_user(user_data):
    latest_created_at = datetime.datetime.strptime(
        user_data["status"]["created_at"], "%Y-%m-%d %H:%M:%S")
    if user_data["default_profile_image"]:
        return True
    elif 2019 > int(latest_created_at.strftime("%Y")):
        return True
    elif 6 > int(user_data["statuses_count"]):
        return True
    return False


followers_ids = []
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, timeout=200, wait_on_rate_limit=True,
                 retry_count=2, retry_delay=5, wait_on_rate_limit_notify=True)
my_id = api.me()._json["id"]
for user_id in tweepy.Cursor(api.followers_ids, id=my_id).items():
    followers_ids.append(user_id)
for user_id in followers_ids:
    user_data = api.get_user(user_id)._json
    if judge_user(user_data):
        api.create_block(user_id)
