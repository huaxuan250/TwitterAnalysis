import json

'''
Most engaging sentiment/least engaging sentiment (based on likes/retweets)
Most common sentiment/sentiment breakdown (percentage wise)
Times of the day that you tweet (& correlation with sentiment?)
Where do you tweet → (& correlation with sentiment?)
Who you interact with the most > comments, likes, retweets
What topics you tweet most about  which ones got the most engagement
Set of Best tweets/worst tweets
Most loyal followers - who has followed you the longest/liked most of your tweets
'''

user = "metal_gear"


most_engage = "anger"
least_engage = "joy"

senti2percent = {
    "anger":78,
    "sorrow":15,
    "joy":7
}

times = [
    "early morning",
    "early afternoon",
    "late night"
]

locations =[
    "Home",
    "Work"
]

most_interacted = "senator_armstrong"

interests = ["sports", "food", "politics"]
intCount = [12, 32, 108]

intFreq = {}

for i in range(len(interests)):
    intFreq[interests[i]] = intCount[i]

longest = "moreplatesmoredates"

sample = {}


sample["user"] = user
sample["sentiments"] = senti2percent
sample["times"] = times
sample["locations"] = locations
sample["most interacted"] = most_interacted
sample["interests"] = intFreq
sample["longest follower"] = longest

object = json.dumps(sample, indent = 4)
print(object)