from twitter import filter_stream

keywords = ["og", "i", "at", "det", "er", "en", "på", "til", "af", "med", "jeg", "du", "kan"]
languages = ["da"]

def tweet(user, followers, friends, retweet, keyword, text):
    print("{}: {}".format(user, text))

def stats(timestamp, keyword, count):
    print(keyword, count)

filter_stream(tweet, file=__file__, track=keywords, languages=languages)