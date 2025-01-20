import tweepy
from dotenv import load_dotenv
import os
import time
import json  

load_dotenv()

BEARER_TOKEN = os.getenv("BEARER_TOKEN")
client = tweepy.Client(bearer_token=BEARER_TOKEN)

def get_tweets(username, max_results=5):
    """Fetches the latest tweets for a given username,
    retrying if a rate limit (429) error occurs."""
    try:
        # Look up the user by username
        user = client.get_user(username=username)
        user_id = user.data.id
        
        # Fetch the user’s tweets
        response = client.get_users_tweets(
            id=user_id,
            max_results=max_results,
            tweet_fields=["created_at", "text"]
        )
        return response  # This is a tweepy.Response object
    except tweepy.errors.TooManyRequests:
        print("Hit the rate limit. Waiting 15 minutes before retrying...")
        time.sleep(15 * 60)  # 15 minutes = 900 seconds
        # Retry once after waiting
        return get_tweets(username, max_results)
    
def parse_tweet_content(tweet_text):
    """
    Parse lines like:
        3WR 145
        4WR 50
        CM 44
        SPIN 23
        WO 6
    and return a dictionary:
        {
            "3WR": 145,
            "4WR": 50,
            "CM": 44,
            "SPIN": 23,
            "WO": 6
        }
    """
    data_dict = {}
    
    # Each line should be in the format "<key> <number>"
    lines = tweet_text.split('\n')
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 2:
            key, value = parts
            # Try converting the value to an integer
            try:
                data_dict[key] = int(value)
            except ValueError:
                # If it fails, just store the string or ignore
                data_dict[key] = value

    return data_dict

def main():
    username_to_lookup = "WesternWeightRm"
    response = get_tweets(username_to_lookup, max_results=5)
    
    # response might be None or might have an empty .data if the user has no tweets
    tweets_data = response.data if response and response.data else []
    
    parsed_tweets = []
    for tweet in tweets_data:
        # Create a base structure with timestamp
        tweet_obj = {
            "timestamp": str(tweet.created_at)  # Convert datetime to string
        }
        
        # Parse the tweet text for the numeric values
        metrics = parse_tweet_content(tweet.text)
        
        # Merge parsed metrics into the tweet object
        tweet_obj.update(metrics)
        
        parsed_tweets.append(tweet_obj)
    
    # Print them to the console for debugging
    print("Parsed Tweets:")
    for pt in parsed_tweets:
        print(pt)
    
    # Write all tweets to a JSON file
    with open("tweets.json", "w", encoding="utf-8") as f:
        json.dump(parsed_tweets, f, indent=4)

if __name__ == "__main__":
    main()
