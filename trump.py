from twitter import filter_stream

keywords = ["trump"]

def tweet(user, followers, friends, retweet, keyword, text):
    print("{}: {}".format(user, text))

def stats(timestamp, keyword, count):
    print(keyword, count)

filter_stream(tweet, file=__file__, track=keywords)