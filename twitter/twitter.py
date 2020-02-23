import tweepy
import threading
import time
from collections import defaultdict
from datetime import datetime

def generate_callback(track, callback, file):

    stats_output = file.replace(".py","") + ".csv"
    stats = defaultdict(int)

    def loop():
        header = "tidspunkt"
        for query in sorted(track):
            header += ", {}".format(query)
        with open(stats_output, "w+") as f:
            f.write(header + "\n")
        while True:
            for query in track:
                stats[query] += 0
            time.sleep(60)
            line = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for k in sorted(stats.keys()):
                line += ",{}".format(stats[k])
            with open(stats_output, "a") as f:
                f.write(line + "\n")
            stats.clear()

    thread = threading.Thread(target=loop)
    thread.start()

    class MyStreamListener(tweepy.StreamListener):
        def on_status(self, status):

            user = status.user.name
            followers = status.user.followers_count
            friends = status.user.friends_count

            if hasattr(status, "retweeted_status"):
                retweet = True
                try:
                    text = status.retweeted_status.extended_tweet["full_text"]
                except AttributeError:
                    text = status.retweeted_status.text
            else:
                retweet = False
                try:
                    text = status.extended_tweet["full_text"]
                except AttributeError:
                    text = status.text

            keywords = None
            for query in track:
                if all(word in text.lower() for word in query.lower().split()):
                    keywords = query
                    stats[query] += 1


            callback(user, followers, friends, retweet, keywords, text.strip().replace("\n", " "))

        def on_error(self, status_code):
            print("ERROR! STATUS CODE: {}".format(status_code))
            return False

    return MyStreamListener()

def filter_stream(callback, file, track, **kwargs):
    consumer_key = "dHtCQWJdlI7EELnvTYorg"
    consumer_secret = "oOeuKpf4yvBEiHyeUS0oRTgStZvYtKutDLcqbx29VU"
    access_token = "17893704-wQvixZ7eYVSkemn9mag51YioJpzLuch0devAJKp9M"
    access_token_secret = "ngUFy1YqPFTKcbt6QK11THLSNEjPliBfusyqS4mUPa0QD"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    myStream = tweepy.Stream(auth = auth, listener=generate_callback(track, callback, file))
    myStream.filter(track=track, is_async=True, **kwargs)
