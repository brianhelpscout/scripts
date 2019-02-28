import requests, json, re
from trello import Trello
from datetime import datetime
from datetime import timedelta

with open("config.json", "r") as f:
  config = json.load(f)

trello = Trello(config["Trello"])

list_id = trello.get_list_id(name="Done")

cards = trello.get_cards_in_list(list_id=list_id)

fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
start_date = datetime.now() + timedelta(-21)
count = 0
for card in json.loads(cards.text):
    act=card["dateLastActivity"]
    dt=datetime.strptime(act, fmt)
    if any(label["name"] == "CANI" for label in card["labels"]): print("Yes")
    if dt > start_date: count += 1

list_id = trello.get_list_id(name="Deployed")

cards = trello.get_cards_in_list(list_id=list_id)

for card in json.loads(cards.text):
    act = card["dateLastActivity"]
    dt = datetime.strptime(act, fmt)
    if dt > start_date: count += 1

print(count)