# Dirty script to pull a list of PRs from a Trello Board, and pull some
# metadata from github.
#
# Outputs a CSV:
# PR,Author,Opened,Closed/Merged,Notes
#
# See config.json.example for the input variables you need to provide.

import configparser, requests, json, re

with open("config.json", "r") as f:
  config = json.load(f)

trello_config = config["Trello"]

lists_url = "https://api.trello.com/1/boards/{}/lists"
lists_url = lists_url.format(trello_config['BOARDID'])

querystring = {"cards":"open","card_fields":"all","fields":"all",
               "key":trello_config["KEY"],"token":trello_config["TOKEN"]}

response = requests.request("GET", lists_url, params=querystring)
if response.status_code != 200:
  exit("Trello Request Error getting list: {}".format(response.status_code))

list_id = ""
list_name = trello_config["LISTNAME"]
for list in json.loads(response.text):
  if list["name"] == list_name: 
    list_id = list["id"]
    break

if list_id == "": exit("Couldn't find list: {}".format(list_name))

cards_url = "https://api.trello.com/1/lists/{}/cards".format(list_id)

querystring = { "attachments":"true",
                "attachment_fields":"all",
                "key":trello_config["KEY"],
                "limit":1000,
                "token":trello_config["TOKEN"]}

cards = requests.request("GET", cards_url, params=querystring)
if cards.status_code != 200:
  exit("Trello Request Error getting cards: {}".format(cards.status_code))

urls = []
for card in json.loads(cards.text):
  for attachment in card["attachments"]:
    url = attachment["url"]
    if "github" in url and url not in urls:
      urls.append(url)

if(len(urls) == 0): exit("No URLS found!")

# GET /repos/:owner/:repo/pulls/:number
github_url = "https://api.github.com/repos/{owner}/{repo}/pulls/{number}"

regex_expr = "github\.com\/(?P<owner>\w*)\/(?P<repo>.*)\/pull\/(?P<num>\d*)"
user = config["GitHub"]["USER"]
token = config["GitHub"]["TOKEN"]
results = []
authors = {}

def add_author(author_id, authors, url):
  if author_id not in authors:
    response = requests.request("GET", url, auth=(user, token))
    a = json.loads(response.text)
    authors[author_id] = a["name"]
  return authors

for url in urls:
  match = re.search(regex_expr, url)
  pr_url = github_url.format(owner=match.group("owner"),
                             repo = match.group("repo"),
                             number=match.group("num")
                            )
  response = requests.request("GET", pr_url, auth=(user, token))
  pr = json.loads(response.text)
  author_id = pr["user"]["id"]
  authors = add_author(pr["user"]["id"], authors, pr["user"]["url"])
  
  results.append({"url":url,
                  "title": pr["title"],
                  "author":authors[author_id],
                  "opened":pr["created_at"],
                  "merged": pr["merged"],
                  "merged_at": pr["merged_at"],
                  "closed_at": pr["closed_at"]
                 })

from datetime import datetime

def get_date(input):
  date_obj = datetime.strptime(input, "%Y-%m-%dT%H:%M:%SZ")
  return datetime.strftime(date_obj, "%m/%d")

output = open("output.csv", "w")
output.write("PR,Author,Opened,Closed/Merged,Notes\n")
for result in results:
  output.write("{} {}".format(result["url"], result["title"]))
  output.write(",")
  output.write(result["author"])
  output.write(",")
  output.write(get_date(result["opened"]))
  output.write(",")
  if "true" == result["merged"]:
    output.write(get_date(result["merged_at"]))
  else:
    output.write(get_date(result["closed_at"]))
  output.write(",")
  output.write("\n")
output.close()
