# Simple script to pull all the unique PRs from a Trello board JSON export
import argparse, json

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=argparse.FileType('r'))
args = parser.parse_args()

data = json.load(args.input)

done_list = "Not Found"
for list in data['lists']:
  if 'Done' == list['name']:
    done_list = list['id']
    break;

print("Done List ID: " + done_list)

# Pull all the github urls from the cards themselves.
urls = []
for card in data['cards']:
  if done_list != card['idList']:
    continue;
  for attachment in card['attachments']:
    if 'github' in attachment['url'] and attachment['url'] not in urls:
      urls.append(attachment['url'])

# Scan the action list to see if the PR has a description, and append it.
results = urls.copy()
for action in data['actions']:
  if (action['type'] == 'addAttachmentToCard' and
        'url' in action['data']['attachment'].keys() and
        'github' in action['data']['attachment']['url'] and
        action['data']['attachment']['name'].startswith('#') and
        action['data']['attachment']['url'] in urls):
    attachment = action['data']['attachment']
    url = attachment['url']
    print(url)
    pos = results.index(url)
    results.pop(pos)
    results.insert(pos, url + ' ' + attachment['name'])
    urls.remove(url)

# Write the results to the output file.
output = open('output.csv', 'w')
for result in results:
  output.write(result+'\n')
output.close()

