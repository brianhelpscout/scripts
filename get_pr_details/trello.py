import requests, json
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Trello:
    def __init__(self, config):
        self.board_id = config["BOARDID"]
        self.key = config["KEY"]
        self.token = config["TOKEN"]

    def get_list_id(self, name):
        lists_url = "https://api.trello.com/1/boards/{}/lists"
        lists_url = lists_url.format(self.board_id)

        querystring = {"cards": "open", "card_fields": "all", "fields": "all",
                       "key": self.key, "token": self.token}

        response = requests.request("GET", lists_url, params=querystring)

        if response.status_code != 200:
            raise Exception("Trello Request Error getting list: {}".format(response.status_code))

        list_id = ""
        for list in json.loads(response.text):
            if list["name"] == name:
                list_id = list["id"]
                break

        if list_id == "": raise Exception("Couldn't find list: {}".format(list_name))
        return list_id

    def get_cards_in_list(self, list_id):
        cards_url = "https://api.trello.com/1/lists/{}/cards".format(list_id)

        querystring = {
                       "attachments": "true",
                       "attachment_fields": "all",
                       "key": self.key,
                       "limit": 1000,
                       "token": self.token}

        cards = requests.request("GET", cards_url, params=querystring)
        if cards.status_code != 200:
            raise Exception("Trello Request Error getting cards: {}".format(cards.status_code))

        return cards