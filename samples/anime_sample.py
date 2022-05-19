import json

interests = ["sports", "food", "politics"]
intCount = [12, 32, 108]

intFreq = {}

for i in range(len(interests)):
    intFreq[interests[i]] = intCount[i]

accounts = ["iusearchbtw", "gnuisnotunix", "senator_armstrong"]

activeMethod = ["comments"]

longest = "moreplatesmoredates"

mostActive = ["nanomachines_son", "cibola_burn", "memorys_legion"]

hashtags = ["#EldenRing", "#Nanomachines", "#ArchLinux"]

activity = "More Active"

followerCount = "Above Average"

sample = {}

sample["interests"] = intFreq
sample["Most Interacted Accounts"] = accounts
sample["Most Active Method"] = activeMethod
sample["Longest Follower"] = longest
sample["Most Active Followrs"] = mostActive
sample["Hashtags"] = hashtags
sample["Active Level"] = activity
sample["Follower Count Level"] = followerCount

object = json.dumps(sample, indent = 4)
print(object)