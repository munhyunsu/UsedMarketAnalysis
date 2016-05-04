from tlib.personal import CUSTOMER_KEY, CUSTOMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET
import tweepy
import urllib3
import certifi

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key = CUSTOMER_KEY
consumer_secret = CUSTOMER_SECRET

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token = ACCESS_TOKEN
access_token_secret = ACCESS_SECRET

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

# If the authentication was successful, you should
# see the name of the account print out
#print(api.me())
search_limit = api.rate_limit_status()['resources']['users']['/users/search']['remaining']

# If the application settings are set for "Read and Write" then
# this line should tweet out the message to your account's
# timeline. The "Read and Write" setting is on https://dev.twitter.com/apps
#api.update_status(status='Updating using OAuth authentication via Tweepy!')

# If remain
if(search_limit > 0):
	search_user = api.search_users('LunaticHarmony', 20, 1)
	print '[' + str(search_limit) + ']', search_user
