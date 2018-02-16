import requests 
r = requests.get("https://news.ycombinator.com/newest")
print(r.ok)
print(r.text[:100])