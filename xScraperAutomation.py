import asyncio
from twikit import Client
import json
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin with your service account key.
# Replace 'path/to/serviceAccountKey.json' with the path to your downloaded JSON file.
cred = credentials.Certificate('westernrec-d2371-firebase-adminsdk-fbsvc-8554f1bf93.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

async def main():
    client = Client('en-US')
    
    # Log in (ensure you await async functions)
    await client.login(
        auth_info_1='westerngym1878',
        password='Redbirds#11'
    )
    
    # Save and load cookies (if these are synchronous, calling them directly is fine)
    client.save_cookies('cookies.json')
    client.load_cookies(path='cookies.json')
    
    # Fetch the user and tweets asynchronously.
    user = await client.get_user_by_screen_name('WesternWeightRm')
    tweets = await user.get_tweets('Tweets', count=5)
    
    # Optionally, create a list for local storage (if you want to later write to CSV/JSON)
    tweets_to_store = []
    
    # Firestore collection where tweets will be stored.
    tweets_collection = db.collection('tweets')
    
    for tweet in tweets:
        # Transform your tweet data into the desired format.
        # Here, we assume you can extract the following values from the tweet.
        # You may need to adjust these fields based on your tweet object's attributes.
        tweet_data = {
            'timestamp': tweet.created_at,  # Assuming tweet.created_at is a proper timestamp string.
            '3WR': getattr(tweet, '3WR', None),    # Replace 'threeWR' with the correct attribute or parsing logic.
            '4WR': getattr(tweet, '4WR', None),     # Replace 'fourWR' with the correct attribute.
            'CM': getattr(tweet, 'CM', None),          # Replace 'CM' with the correct attribute.
            'SPIN': getattr(tweet, 'SPIN', None),      # Replace 'SPIN' with the correct attribute.
            'WO': getattr(tweet, 'WO', None)           # Replace 'WO' with the correct attribute.
        }
        
        # Add tweet data to Firestore.
        # Optionally, if the tweet object has a unique id (e.g., tweet.id), you can use it as the document ID.
        if hasattr(tweet, 'id'):
            tweets_collection.document(str(tweet.id)).set(tweet_data)
        else:
            tweets_collection.add(tweet_data)
        
        # Append to local list if needed.
        tweets_to_store.append(tweet_data)
        
        # Print each tweet document in the desired format.
        print(tweet_data)
        
    # Print the JSON representation.
    print(json.dumps(tweets_to_store, indent=4))

# Run the asynchronous main function.
asyncio.run(main())
