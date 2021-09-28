import tweepy, os, random, srt
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

def interact(query=default, count=5, RT=True):
    # search for tweets based on given query
    result = api.search_tweets(query, count=count, result_type="recent")
    print(f"-------------------------\nSearching for {query}...")
    print(f"-------------------------\nFound {len(result)} results!")

    N = min(count, len(result))
    # iterate through found tweets
    for i in range(N):
        # organize data
        info = result[i]._json
        username = info['user']['screen_name']
        text = result[i]._json['text'] 
        tweet_id = info['id']
        user_id = info['user']['id']

        print(f'-------------------------\n#{i+1} found:')
        print(f'@{username}:')
        print(text)

        hashtags = [h['text'] for h in info['entities']['hashtags']]

        # check if tweet was already liked and/or retweeted before doing so
        status = api.get_status(tweet_id)
        if username == "agabotto_":
            print("Won't interact with own tweet.")
        else:
            if not status.favorited:
                api.create_favorite(tweet_id)
                print("Just liked!")
            else:
                print("Tweet was already liked.")

            if not status.retweeted and RT:
                api.retweet(tweet_id)
                print("Just retweeted!")
            elif status.retweeted:
                print("Tweet was already retweeted.")
            elif not RT:
                print("Won't RT the enemy.")


def generate_text():
    with open("text/source.srt", "r") as file:
        source_text = file.read()

    subtitle_generator = srt.parse(source_text)
    subtitles = list(subtitle_generator)

    line = random.choice(range(len(subtitles)+1))
    text = subtitles[line].content

    hashtags = ['casaAgamotto', 'semcompou', 'semcomp24', 'semcomp']
    random.shuffle(hashtags)
    status = f"{text} #{hashtags[0]} #{hashtags[1]} #{hashtags[2]} #{hashtags[3]}"

    print(status)
    tweet(status)

generate_text()

# Agamotto (like + RT)
interact(default, 20)

# other tweets (only like)
more_hashtags = ['semcomp', 'semcompou', 'semcomp24', 'casaOcarina', 'casaTardis', 'casaDelorean']
query = random.choice(more_hashtags)
interact(f'#{query}', 15, False)
