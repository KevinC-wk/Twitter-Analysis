import tweepy
from tweepy import OAuthHandler, Stream
from textblob import TextBlob
import dataset
import json
import csv
import re
import unicodedata
from tweepy_utils import get_text_sanitized, get_coords

import config

auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)
 
api = tweepy.API(auth)


class StreamListener(tweepy.StreamListener):

    def __init__(self, num_tweets):
        self.counter = 0
        self.num_tweets = num_tweets
        self.db = dataset.connect("sqlite:///tweets.db")


    """
    def on_status(self, status):
        if status.retweeted_status:
            return
        print(status)

        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color
        blob = TextBlob(text)
        sent = blob.sentiment

        if coords is not None:
            coords = json.dumps(coords)

        table = self.db["tweets"]
        table.insert(dict(
            user_description=description,
            user_location=loc,
            coordinates=coords,
            text=text,
            user_name=name,
            user_created=user_created,
            user_followers=followers,
            id_str=id_str,
            created=created,
            retweet_count=retweets,
            user_bg_color=bg_color,
            polarity=sent.polarity,
            subjectivity=sent.subjectivity,
            ))

        self.counter += 1
        if self.counter == self.num_tweets:
            return False
        print(status.text)
    """

    def on_error(self, status_code):
        if status_code == 420:
            return False


    def extract_data(self, tweet):
        return

    #self.keys = ['created_at', 'text', 'coords(as tuple)', user['followers_count'], user['friends_count'], user['verified'],
    #            user['location'], user['created_at'], 'retweet_count', 'favorite_count', user['id_str']]
    def on_data(self, data):
        try:
            parsed = json.loads(data)
            user = parsed['user']
            text = get_text_sanitized(parsed)
            blob = TextBlob(text)
            sent = blob.sentiment
            print(user['id_str'])

            if parsed['lang'] == 'en' and 'retweeted_status' not in parsed:
                with open('data.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([user['id_str'], text, parsed['created_at'], get_coords(parsed),
                                     user['followers_count'], user['friends_count'], user['verified'], user['location'],
                                     user['created_at'], parsed['retweet_count'], parsed['favorite_count'],
                                     sent.polarity, sent.subjectivity])
                    return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True


if __name__ == "__main__":
    twitter_stream_listener = StreamListener(10)
    twitter_stream = Stream(auth=auth, listener=twitter_stream_listener)
    twitter_stream.filter(track=['#trump'])
