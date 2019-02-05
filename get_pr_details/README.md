# get_pr_details.py

Simple script to generate a CSV with details of all the PRs associated with a list on a Trello board. Not very fancy, missing error handling, etc., but useful to generate a CSV that contains a list of PRs for a Trello list.  The CSV will contain:

PR: A link to the PR followed by the PR name
Author: Who opened the PR
Opened: When it was opened
Closed/Merged: When it was closed or merged
Notes: Empty for now, but a place where you can add notes when you import the data into a table. :-)

Usage: pipenv run python get_pr_details.py

It will write the data into output.csv

A sample config file is provided for options you need to provide.  Copy config,json.example to config.json, and provide:

Trello KEY: [You Trello API key](https://trello.com/app-key)
Trello TOKEN: An authorized token for that key (The previous link provides a way to manually generate one).
Trello BOARDID: The ID of the board you want to pull from.  You can get this from the URL for the board.  For example, for the board https://trello.com/b/t7ATDuA3/beacon-21 the ID is t7ATDuA3
Trello LISTNAME: The name of the list with the cards you want to get PR info for (Done for example)

GitHub USER: Your GitHub Username
GitHub TOKEN: A [Personal access token](https://github.com/settings/tokens) for your GitHub User
