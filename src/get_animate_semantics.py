from collections import Counter

### Arguments: data JSON, query String
### Returns: 3 most common of query (users or hashtags)
def search(data, query):

    search_queries = {}

    if query == 'users':
        search_char = '@'
    if query == 'hashtags':
        search_char = '#'

    retweets = data['retweets']

    for retweet in retweets:
        search_query = retweet['text'].split()
        for i in search_query:
            if i[0] == search_char:
                if i in search_queries:
                    search_queries[i] = search_queries[i] + 1
                else:
                    search_queries[i] = 1

    tweets = data['tweets']

    for tweet in tweets:
        search_query = tweet['text'].split()
        for i in search_query:
            if i[0] == search_char:
                if i in search_queries:
                    search_queries[i] = search_queries[i] + 1
                else:
                    search_queries[i] = 1

    k = Counter(search_queries)
    high = k.most_common(3)

    return high

### Arguments: data JSON
### Returns: account_metrics, follower_metrics
def get_metrics(data):

    metrics = data['user_metrics']

    account_metrics = {'listed': metrics['listed_count'], 'tweets': metrics['tweet_count']}
    follower_metrics = {'followers': metrics['followers_count'], 'following': metrics['following_count']}

    return account_metrics, follower_metrics
