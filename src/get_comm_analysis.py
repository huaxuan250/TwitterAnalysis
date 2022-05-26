from transformers import pipeline
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from collections import Counter
nltk.download('vader_lexicon')


def analyze_label(data):
  label2engage = {}
  for tweet in data["tweets"]:
    
    if "labels" not in tweet:
      continue

    simpleSum = 0
    for metric, count in tweet["public_metrics"].items():
      simpleSum += count
    
    for label in tweet["labels"]:

      if label in ['Brand Vertical', 'Brand Category', 'Events [Entity Service]']:
        continue

      if label not in label2engage:
        label2engage[label] = simpleSum
      else:
        label2engage[label] += simpleSum

  labelFreq = sorted(label2engage.keys(), key=lambda kv: label2engage[kv])
  if len(labelFreq) < 3:
    labelFreq = labelFreq
  else:
    labelFreq = labelFreq[-3:]
  labelFreq = labelFreq[::-1]

  return label2engage, labelFreq
def analyze_polarity(data):
  sia = SentimentIntensityAnalyzer()
  tweets = data["tweets"]
  pos, neg, comps = [], [], []
  polar_tag = [0, 0, 0]
  for tweet in tweets:
    temp = tweet["text"]
    scores = sia.polarity_scores(temp)
    pos.append(scores["pos"])
    neg.append(scores["neg"])

    comp = scores["compound"]
    comps.append(comp)

    if comp > 0.005:
      polar_tag[0] += 1 # pos
    elif comp < -0.005:
      polar_tag[1] += 1 # neg
    else:
      polar_tag[2] += 1 # neu

  most_pos = tweets[pos.index(max(pos))]["id"]
  most_neg = tweets[neg.index(max(neg))]["id"]
  comp_score = sum(comps)/len(comps)

  return most_pos, most_neg, comp_score, polar_tag
def analyze_timeperiod(data):
  hour2engagement = {}
  for tweet in data["tweets"]:
    date = tweet["created_at"]
    time = date.split("T")[1]
    hour = time.split(":")[0]
    hour = int(hour)
    
    simpleSum = 0
    for metric, count in tweet["public_metrics"].items():
      simpleSum += count

    if hour not in hour2engagement:
      hour2engagement[hour] = simpleSum
    else:
      hour2engagement[hour] += simpleSum
    


  period2engage = {
      "night":0,
      "early morning":0,
      'late morning':0,
      "early afternoon":0,
      "late afternoon":0,
      "early evening":0,
      "late evening":0
  }


  for hour, freq in hour2engagement.items():
    if hour in [23,0,1,2,3,4,5]:
      period2engage["night"] += freq
    elif hour in [6,7,8,9]:
      period2engage["early morning"] += freq
    elif hour in [10,11]:
      period2engage["late morning"] += freq
    elif hour in [12,13]:
      period2engage["early afternoon"] += freq
    elif hour in [14,15,16]:
      period2engage["late afternoon"] += freq
    elif hour in [17,18,19]:
      period2engage["early evening"] += freq
    elif hour in [20,21,22]:
      period2engage["late evening"] += freq
  
  return period2engage
def analyze_sentiments(data):
  classifier = pipeline("text-classification",model='bhadresh-savani/distilbert-base-uncased-emotion', return_all_scores=True)
  tweets = data["tweets"]
  sentFreq = {}
  for tweet in tweets:
    temp = tweet["text"]
    # predict current tweet's sentiment
    pred = classifier(temp)
    pred = sorted(pred[0], key=lambda x: x["score"])
    top_sent = pred[-1]["label"]
    if top_sent in sentFreq:
      sentFreq[top_sent] += 1
    else:
      sentFreq[top_sent] = 1


  # get top-3 sentiments from a user's tweets
  sents = sorted(sentFreq.keys(), key=lambda kv: sentFreq[kv])
  if len(sents) < 3:
    sents = sents
  else:
    sents = sents[-3:]

  sents = sents[::-1]

  return sents, sentFreq
def analyze_hour(data):
  hours = []
  for tstamp in data["timeline"]:
    date = tstamp["created_at"]
    time = date.split("T")[1]
    hour = time.split(":")[0]
    
    hours.append(hour)

  hoursFreq = Counter(hours)
  hoursFreqSorted= sorted(hoursFreq.keys(), key=lambda kv: hoursFreq[kv])
  top3Hours = None

  if len(hoursFreqSorted) < 3:
    top3Hours = hoursFreqSorted
  else:
    top3Hours = hoursFreqSorted[-3:]

  top3Hours = top3Hours[::-1]

  return top3Hours, hoursFreq
def analyze_zealousfan(data):
  user2mentions = data["user_mentions"]
  max_freq = max(user2mentions.values())
  most_interacted = [user for user in user2mentions.keys() if user2mentions[user] == max_freq]
  return most_interacted
def analyze_clouts(data):
  # DO IT FOR THE VINE
  id2clout = {}
  for tweet in data["tweets"]:
    
    simpleSum = 0
    for metric, count in tweet["public_metrics"].items():
      simpleSum += count
    
    id2clout[tweet["id"]] = simpleSum

  idFreq = sorted(id2clout.keys(), key = lambda kv: id2clout[kv])
  mostPopular = idFreq[-1]

  return mostPopular, idFreq

def comm_analyze(data):

  # C1 C7:
  label2engage, labelFreq = analyze_label(data)

  # C2
  most_pos, most_neg, comp_score, polar_tag = analyze_polarity(data)

  # C3
  period2engage = analyze_timeperiod(data)

  # C4:
  sents, sentFreq = analyze_sentiments(data)

  # C5
  top3hours, hoursFreq = analyze_hour(data)

  # C8
  most_interacted = analyze_zealousfan(data)

  #c9
  longest_follower = data["followers"][-1]

  # c10: Most popular Tweet
  mostPopular, idFreq = analyze_clouts(data)

  # A
  newest10followers = data["followers"][10:]
  oldest10followers = data["followers"][-10:]

  # A
  top3tweets = idFreq[-3:]

  '''
  Final Json Construction
  '''
  # Contructing json
  final_output = {}

  # C1: Topic Engage Correlation
  final_output["topic_engagement"] = label2engage

  # C2: Most Positive and negative
  final_output["most_positive_tweet"] = most_pos
  final_output["most_negative_tweet"] = most_neg

  # C3: Time Engage Correlation
  final_output["time_engagement"] = period2engage

  # C4: Top 3 Sentiments
  sentiments = {}
  for sent in sents:
    sentiments[sent] = sentFreq[sent]
  final_output["sentiments"] = sentiments

  # C5: Top 3 Hours:
  activeHours = {}
  for hour in top3hours:
    activeHours[hour] = hoursFreq[hour]
  final_output["active_hours"] = activeHours

  # C7: Topic
  top3engage = {}
  for label in labelFreq:
    top3engage[label] = label2engage[label]
  final_output["top_interests"] = top3engage

  # C8:

  final_output["most_interacted_user"] = most_interacted

  # C9:
  final_output["longest_follower"] = longest_follower

  # C10:
  final_output["most_popular_tweet"] = mostPopular

  # C11:
  final_output["overall_compound_score"] = comp_score

  # C12:
  final_output["polarity_count"] = {
      "positive tweets":polar_tag[0],
      "negative tweets":polar_tag[1],
      "netural tweets":polar_tag[2]
  }


  final_output["top_3_tweets"] = top3tweets

  final_output["newest_10_followers"] = newest10followers
  final_output["oldest_10_followers"] = oldest10followers

  # final_json = json.dumps(final_output, indent = 4)

  return final_output