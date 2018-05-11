INST326 Final Project 

Sam Moon and Grace Zhang

                                                   Twitter Data Anaysis

The purpose of the program we have written is to create a tool to aide with research about social movement phenomemons. Our program allows users to search for recent trending social movements on Twitter, such as #BlackLivesMatter, #MeToo, #TimesUp, etc. Our program scrapes recent data from Twitter using the Tweepy module, and sorts through the data to find the location, frequency of location, user screen name and the relevant tweet containing the hashtag. Allowing the user to see the location and frequency of hashtags will give researchers an important perspective on what influences participation in specific social trends. This tool is extremely relevant and useful given our current political climate. 

Instructions:

1. The program will prompt the user to input the desired hashtag movement they are looking for. Enter the movement along with the '#' symbol. For example: #Blacklivesmatter, #MeToo, #Notmypresident

2. The program will prompt the user for the number of data entries they want to recieve. Please enter a number that is greater than 0. 

3. Next, the program will run. Give the program time to run and it will finish by displaying 'Process finished with exit code 0'. 

4. Then, you will open the folder that the program is located in, and you will find the TWO output files named: 'tweet_data' and 'tweets_by_timezone'. 

5. Open 'tweet_data': it will display the timezone and frequency of how many people tweeted from that timezone. 

6. Open 'tweets_by_timezone': it will display the timezone, screen name of the Twitter user, and their tweet containing the hashtag. 

7. Analyze the data as it pertains to your research. 

**NOTE** if you recieve this error message: 'tweepy.error.TweepError: Twitter error response: status code = 429', the program is NOT broken- it simply means that the Tweepy data limit has been reached. If you wait for 15 minutes, the limit will be reset and you can test the code again. 
