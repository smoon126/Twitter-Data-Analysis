# Sam Moon, Grace Zhang
# Final Project
# Twitter Data Analysis

# Importing necessary modules
import tweepy
import csv


# Main class
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

        # Our class instance hashtag query variable
        self.query = query

        # The number of data points we want per data set
        self.data_points = data_points

        # A running list of the unique ID's of tweets we come across, this becomes helpful for making sure we do not
        # have a duplicate tweet in multiple data sets.
        self.ids = list()

        # Counters for how many times we've exported data to CSV so that we can have unique file names for every
        # export
        self.counter0 = 0
        self.counter1 = 0

        # Our twitter data, data structure. At the top level this is a String, List key, value dictionary where the key
        # is the time zone and the List is a list of dictionaries containing tweets that were posted from the
        # respective time zone. The dictionaries within the lists are String, String dictionaries where the keys are
        # user twitter screen names and the values are the respective text of their tweets.
        self.data = {}

        # The initial data pull from twitter.
        self.get_data_batch()

    # Retrieving data from Twitter
    def get_data_batch(self):
        # Initializing the data structure that will hold the data
        self.data = {}

        # Local variable that acts as a counter for how many valid data points we've sifted through
        data_length = 0

        # The while condition ensures we keep finding data points until we have the specified amount
        while data_length < self.data_points:

            # We first get a very large batch of tweets to sift through for valid data points
            # We get a large batch to worth with because the Twitter API rate limits requests based on 15 min intervals
            # See: https://developer.twitter.com/en/docs/basics/rate-limiting
            data_batch = tweepy.Cursor(self.api.search, q=self.query, lang='en', show_user='true').items(1000)

            # Loop that verifies the data usability of each tweet
            for tweet in data_batch:

                # This try/catch block is used to accommodate to the tweepy "Status" data structure that is used to
                # parse data from the twitter API. The try block is specifically used to filter out retweets from
                # original tweets. Each tweet object has a retweeted_status attribute that does not exist if it is an
                # original tweet and does exist if it is a retweet. When we check whether or not this data block exists,
                # if the retweet block does not exist in the if statement in the try block, an attribute error is thrown
                # This confirms for us that the tweet is formatted with original tweet data so we can catch this error
                # and process data in the catch block.
                try:
                    # If the tweet is not an original tweet or if it has been viewed before or if there is no timezone
                    # data specified, it is ignored
                    if tweet.id in self.ids or tweet.author.time_zone is None \
                            or tweet.retweeted_status.text is not None:
                        pass

                # Confirmed that the data is valid
                except AttributeError:

                    # Entering valid data into dictionaries on the condition that we do not have enough data yet
                    if data_length < self.data_points:

                        # Creating our String, List of dictionaries data stucture
                        if tweet.author.time_zone not in self.data:
                            self.data[tweet.author.time_zone] = [{tweet.author.screen_name: tweet.text}]
                        else:
                            self.data[tweet.author.time_zone].append({tweet.author.screen_name: tweet.text})

                        # Incrementing that we have successfully inputted a data point and increased the size of the
                        # data structure
                        data_length += 1
                    else:
                        # Triggers only when we have enough data
                        break

                # After we've seen a tweet we make sure it is never used again
                self.ids.append(tweet.id)

    '''Everything from here up was written by Grace, everything below was written by Sam'''

    # The two methods below are in logic identical so only this one will be rigorously explained
    def create_tweet_by_timezone_csv(self):

        # Explicitly defining the CSV file data columns since they will always be the same
        csv_columns = ['Timezone', 'Screen Name', 'Tweet Text']

        with open('tweets_by_timezone' + str(self.counter0), 'w', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()

            # Iterating through every tweet in the timezone key's value list of dictionaries and writing them each per
            # row.
            for k, v in self.data.items():
                for tweet in v:
                    for j, z in tweet.items():
                        writer.writerow({csv_columns[0]: k, csv_columns[1]: j, csv_columns[2]: z})

            # The counter is incremented so the next call to this function produces a unique file and does not o/w
            self.counter0 += 1

    # Creating a CSV file that writes the data of how many tweets were in each time zone from the data gathered.
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

# Creating instance of class and calling functions
x = TweetTimeZoneData(user_query, int(num_entries))
x.create_timezone_frequency_csv()
x.create_tweet_by_timezone_csv()

# Testing to see if a new data batch of unique tweets is pulled off the API, it works correctly in this test
x.get_data_batch()
x.create_timezone_frequency_csv()
x.create_tweet_by_timezone_csv()
