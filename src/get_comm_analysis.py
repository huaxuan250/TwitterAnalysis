import pandas as pd
import json
import numpy as np
from transformers import pipeline
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer





def main():
  with open('../samples/output.json') as json_file:
      data = json.load(json_file)


  # C1: Labels and metric correlation
  label2engage = {}
  for tweet in data["tweets"]:
    
    #calculating engagement: simple sum:
    simpleSum = 0
    for metric, count in tweet["public_metrics"].items():
      simpleSum += count
    
    
    #record the frequency:
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

  #C2
  from transformers import pipeline
  classifier = pipeline("text-classification",model='bhadresh-savani/distilbert-base-uncased-emotion', return_all_scores=True)
  nltk.download('vader_lexicon')
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
  most_pn = [most_pos, most_neg]

  comp_score = sum(comps)/len(comps)

  #C3
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

  #C4:
  top3 = {}
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


  # C5
  from collections import Counter

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


  #c7
  # print(labelFreq)

  # C8
  user2mentions = data["user_mentions"]
  max_freq = max(user2mentions.values())
  most_interacted = [user for user in user2mentions.keys() if user2mentions[user] == max_freq]
  # print(most_interacted)

  #c9
  followers = data["followers"]
  longest_follower = followers[-1]


  # c10: Most popular Tweet
  bestTweetId = None

  id2clout = {}
  for tweet in data["tweets"]:
    
    simpleSum = 0
    for metric, count in tweet["public_metrics"].items():
      simpleSum += count
    
    id2clout[tweet["id"]] = simpleSum

  idFreq = sorted(id2clout.keys(), key = lambda kv: id2clout[kv])
  mostPopular = idFreq[-1]

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
  final_output["most_positive_tweet"] = most_pn[0]
  final_output["most_negative_tweet"] = most_pn[1]

  # C3: Time Engage Correlation
  final_output["time_engagement"] = period2engage

  # C4: Top 3 Sentiments
  sentiments = {}
  for sent in sents:
    sentiments[sent] = sentFreq[sent]
  final_output["sentiments"] = sentiments

  # C5: Top 3 Hours:
  activeHours = {}
  for hour in top3Hours:
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

  final_json = json.dumps(final_output, indent = 4)
  with open("comm_output.json", "w") as f:
    json.dump(final_output, f, indent = 4)


main()