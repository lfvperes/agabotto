import datetime, tweepy, os
from dotenv import load_dotenv

load_dotenv()   # loading environment variables

# calculate how many days remain for G-day
def countdown(today):
    # current year
    this_year = today.year

    # start as this year's G-day
    g_day = datetime.datetime(this_year, 2, 2, 23, 59, 59)

    # if G-day is past, update the year by 1, otherwise does not change
    g_day = g_day.replace(year=this_year + (g_day < today))
    # time remaining for the next G-day
    remaining = (g_day - today).days

    return remaining

# based on today's date and on equinox/solstice dates, returns a string
# containing the current season's name
def season(today):
    this_year = today.year

    # dates for each equinox and solstice
    spring = datetime.datetime(this_year, 3, 20)
    summer = datetime.datetime(this_year, 6, 21)
    autumn = datetime.datetime(this_year, 9, 22)
    winter = datetime.datetime(this_year, 12, 21)

    if today < spring:      # before spring equinox
        return 'winter ⛄'
    elif today < summer:    # after spring equinox, before summer solstice
        return 'spring 🌱'
    elif today < autumn:    # after summer solstice, before autumn equinox
        return 'summer 🌞'
    elif today < winter:    # after autumn equinox, before winter solstice
        return 'autumn 🍂'
    else:                   # after winter solstice
        return 'winter ⛄'

auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
auth.set_access_token(os.environ['TWITTER_TOKEN_KEY'], os.environ['TWITTER_TOKEN_SECRET'])

api = tweepy.API(auth)

def tweet(today):
    # get countdown and season name to know what to write
    remaining = countdown(today)
    season_name = season(today)

    if remaining == 0:
        status = "It's Groundhog Day!\n#GroundhogDay"
        filename = 'img/phil.gif'
    else:
        # formatting date as 'Weekday, Month dd yyyy'
        today_text = today.strftime("%A, %B %d %Y")
        # template to be formatted and tweeted
        template = "Punxsutawney Phil says: {1} days until #GroundhogDay!\nIt's {0}. \n#{2}"
        status = template.format(today_text, remaining, season_name)
        # select picture according to season
        filename = 'img/{}.jpg'.format(season_name[:-2])
    
    # upload media and get media ID before tweeting
    media_id = api.media_upload(filename).media_id_string
    # tweet the given text and image
    api.update_status(status, media_ids=[media_id])
    print('Just tweeted "{}"'.format(status))


# today's date
today = datetime.datetime.now()

tweet(today)