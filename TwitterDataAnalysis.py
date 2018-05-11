# Sam Moon, Grace Zhang
# Final Project
# Twitter Data Analysis

# Importing necessary modules
import tweepy
import csv


# Creating main class
class TweetTimeZoneData:

    # Initializing variables/ providing authentication
    def __init__(self, query, data_points):
        consumer_key = "7qrZ20UK6kLy8Ns6Gk7t8vR0O"
        consumer_secret = "xlDpDk32auwwY5RosrkpkCkxgDy4kvUvSj2jhR161rrN7BJ9c8"
        access_token = "993643698037641216-5OLZqnChmNy0YlOKLp9STNkXPAPD0xV"
        access_token_secret = "6cM2f7nBTh8M99bDUT2ExSphnAtmDSynbhrpgfxPuh6iy"

        # Creating the authentication object
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        # Setting your access token and secret
        auth.set_access_token(access_token, access_token_secret)
        # Creating the API object while passing in auth information
        self.api = tweepy.API(auth)

        self.query = query
        self.data_points = data_points
        self.ids = list()
        self.counter0 = 0
        self.counter1 = 0

        # Reset on every call of get_data_batch
        self.data = {}
        self.get_data_batch()

    # Retrieving data
    def get_data_batch(self):
        self.data = {}

        data_length = 0

        while data_length < self.data_points:
            data_batch = tweepy.Cursor(self.api.search, q=self.query, lang='en', show_user='true').items(1000)

            for tweet in data_batch:
                try:
                    # If the tweet is not an original tweet or if it has been viewed before, it is ignored
                    if tweet.id in self.ids or tweet.author.time_zone is None \
                            or tweet.retweeted_status.text is not None:
                        pass
                except AttributeError:
                    if data_length < self.data_points:
                        if tweet.author.time_zone not in self.data:
                            self.data[tweet.author.time_zone] = [{tweet.author.screen_name: tweet.text}]
                        else:
                            self.data[tweet.author.time_zone].append({tweet.author.screen_name: tweet.text})
                        data_length += 1
                    else:
                        break
                self.ids.append(tweet.id)

    '''Everything from here up was written by Grace, everything below was written by Sam'''

    # Entering data into output file
    def create_tweet_by_timezone_csv(self):
        csv_columns = ['Timezone', 'Screen Name', 'Tweet Text']

        with open('tweets_by_timezone' + str(self.counter0), 'w', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for k, v in self.data.items():
                for tweet in v:
                    for j, z in tweet.items():
                        writer.writerow({csv_columns[0]: k, csv_columns[1]: j, csv_columns[2]: z})

            self.counter0 += 1

    # Entering data into output file
    def create_timezone_frequency_csv(self):
        csv_columns = ['Timezone', 'Frequency']

        with open('tweet_data_' + str(self.counter1), 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for k, v in self.data.items():
                writer.writerow({csv_columns[0]: k, csv_columns[1]: v.__len__()})

            self.counter1 += 1


# Prompting for user input
user_query = input("Enter hashtag query: ")
num_entries = input("How many entries do you want: ")

# Basic error check for invalid input
while int(num_entries) <= 0:
    print("Please enter non-zero value.")
    num_entries = input("How many entries do you want: ")

x = TweetTimeZoneData(user_query, int(num_entries))
x.create_timezone_frequency_csv()
x.create_tweet_by_timezone_csv()
x.get_data_batch()
x.create_timezone_frequency_csv()
x.create_tweet_by_timezone_csv()
