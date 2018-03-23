import tweepy
from tweepy import OAuthHandler, Stream
import config

auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)
 
api = tweepy.API(auth)


class StreamListener(tweepy.StreamListener):

    def __init__(self, num_tweets):
        self.counter = 0
        self.num_tweets = num_tweets

    def on_status(self, status):
        self.counter += 1
        if self.counter == self.num_tweets:
            return False
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def on_data(self, data):
        try:
            with open('data.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

if __name__ == "__main__":
    twitter_stream = Stream(auth, StreamListener(10))
    twitter_stream.filter(track=['#trump'])
