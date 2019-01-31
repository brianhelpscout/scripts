# Simple script to pull all the unique PRs from a Trello board JSON export
import argparse, json

parser = argparse.ArgumentParser()
parser.add_argument('input', type=argparse.FileType('r'))
args = parser.parse_args()

urls = []
data = json.load(args.input)
for card in data["cards"]:
  for attachment in card["attachments"]:
    if "github" in attachment["url"] and attachment["url"] not in urls:
      urls.append(attachment["url"])

output = open("output.csv", "w")
for url in urls:
  output.write(url+"\n")
output.close()

