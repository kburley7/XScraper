from apify_client import ApifyClient

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_e7pdqBr0BJNRTSChjxjrwB0fZULNcg3khrFK")

# Prepare the Actor input
run_input = {
    "twitterHandles": [
        "WesternWeightRm",
    ],
    "maxItems": 10,
    "sort": "Latest",
    "tweetLanguage": "en",
    "start": "2025-03-02",
    "end": "2025-03-03",
}

# Run the Actor and wait for it to finish
run = client.actor("61RPP7dywgiy0JPD0").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)