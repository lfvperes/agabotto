import datetime, tweepy, os
from dotenv import load_dotenv

load_dotenv()   # loading environment variables

auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
auth.set_access_token(os.environ['TWITTER_TOKEN_KEY'], os.environ['TWITTER_TOKEN_SECRET'])

# print(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'],os.environ['TWITTER_TOKEN_KEY'], os.environ['TWITTER_TOKEN_SECRET'])

api = tweepy.API(auth)
# client = tweepy.Client()

def tweet(text=''):
    status = text if text else "#casaAgamotto #semcomp24 #semcompou"
    
    # tweet the given text and image
    api.update_status(status)
    print('Just tweeted "{}"'.format(status))

default = "#casaAgamotto"

def interact(query=default, count=5):
    # search for tweets based on given query
    result = api.search_tweets(query, count=count, result_type="recent")

    # iterate through found tweets
    for i in range(count):
        # organize data
        info = result[i]._json
        username = info['user']['screen_name']
        text = result[i]._json['text'] 
        tweet_id = info['id']
        user_id = info['user']['id']

        print('-------------------------\nfound:')
        print(username)
        print(text)

        # check if tweet was already liked and/or retweeted before doing so
        status = api.get_status(tweet_id)
        if not status.favorited:
            api.create_favorite(tweet_id)
            print("Just liked!")
        else:
            print("Tweet was already liked.")

        if not status.retweeted:
            api.retweet(tweet_id)
            print("Just retweeted!")
        else:
            print("Tweet was already retweeted.")


interact(default,10)
