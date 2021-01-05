
import api_gen
import tweepy
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
    elif 6 > int(user_data["followers_count"]):
        return True
    return False


def get_follower_ids(api, uid):
    id_list = []
    for user_id in tweepy.Cursor(api.followers_ids, id=my_id).items():
        id_list.append(user_id)
    return id_list


api = api_gen.api
my_id = api.me()._json["id"]
followers_ids = get_follower_ids(api, my_id)
for user_id in followers_ids:
    user_data = api.get_user(user_id)._json
    if judge_user(user_data):
        api.create_block(user_id)
