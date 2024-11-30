import json
import requests
import re

from src.api_keys import *      # <- gitignored. Contains personal API keys
from src.request_cleanup import *

class RacingMikeAPI():
    def __init__(self):
        self.name = "RacingMikeAPI"
        self.base_url = "https://api.micheleberardi.com/racing/v1.0/"
        self.token = RacingMikeAPI_key

        # {topic:   endpoint,
        #           params,
        #           headers}
        self.requests = {
            "riders":       ["motogp-world-standing-riders",
                            {"year": "2024",
                             "categoryid": "e8c110ad-64aa-4e8e-8a86-f2f152f6a942"},
                             {"accept": "*/*"}],    # motogp, moto2, moto3, motoE
            "events":       ["motogp-events",
                             {"year": "2024"},
                             {"accept": "*/*"}],
            # "sprint-race":  ["motogp-sessions-spr",
            #                  {"year": "2024"},
            #                  {"accept": "*/*"}],
            "results":      ["motogp-full-results",
                             {"eventid": "8ed52491-e1aa-49a9-8d70-f1c1f8dd3090",
                              "year": "2024",
                              "session": "af960ae0-845e-4fac-a431-4a7ea6c7d128"},
                             {"accept": "*/*"}],    # RAC FP1 FP2 FP3 FP4 Q1 Q2 WUP SPR
            "calendar":     ["motogp-calendar",
                             {"filter": "full"},
                             {"accept": "*/*"}],
            # TODO: handle case where season is over (hence, "upcoming" event will be empty) but we still want to use the API handle.
            # "next_event":   ["motogp-calendar",
            #                  {"filter": "upcoming"},
            #                  {"accept": "*/*"}],
        }
    
        self._requests = {
            "categories":   ["motogp-category",
                             {"year": ""},
                             {"accept": "*/*"}],
            "season":       ["motogp-season",
                             {"year": ""},
                             {"accept": "*/*"}],
            }

    @property
    def topics(self):
        return list(self.requests.keys())



class RapidAPI():
    def __init__(self):
        self.name = "RapidAPI"
        self.base_url = "https://motogp-news.p.rapidapi.com"
        self.token = RapidAPI_key

        # {topic:   endpoint,
        #           params,
        #           headers}
        self.requests = {
            "news":         ["/motogpnews/",
                             {},
                             {"x-rapidapi-key": "36365c3e79msha845393c2dbbf94p168759jsn016976429d16",
                              "x-rapidapi-host": "motogp-news.p.rapidapi.com"}]
        }
    
    @property
    def topics(self):
        return list(self.requests.keys())


class Collector():
    def __init__(self):
        pass

    @property
    def apis(self):
        mikeapi = RacingMikeAPI()
        rapidapi = RapidAPI()
        return {"mikeapi": mikeapi,
                "rapidapi": rapidapi}

    @property
    def topics(self):
        topics = []
        for api in list(self.apis.values()):
            for topic in list(api.requests.keys()):
                topics.append(topic)
        return topics

    # given topic as string, find which API it belongs to
    def _find_api_from_topic(self, topic):
        for api in list(self.apis.values()):
            if topic in api.topics:
                return api
        raise Exception(f"No API found with topic `{topic}`!")

    # generic function for sending API requests
    def _request(self, url, endpoint, token, parameters=None, headers=None):
        parameters["token"] = token
        response = requests.get(url + endpoint,
                                params=parameters,
                                headers=headers)
        json_response = response.json()

        if endpoint == "/motogpnews/":
            for entry in json_response["MotoGPNews"]:
                for delete_item in news_delete:
                    del entry[delete_item]
                temp = entry["description"]
                entry["description"] = entry["description"][:temp.index("<a class=")]

        return json.dumps(json_response, indent=2)

    # given topic, retrieve the parameters and get content
    def get_conent_from_topic(self, topic, year):
        api = self._find_api_from_topic(topic)
        endpoint, params, headers = api.requests[topic]
        params["year"] = year
        return self._request(url=api.base_url, endpoint=endpoint, token=api.token, parameters=params, headers=headers)

    def get_season_id(self, year):
        # year between 1949 and 2024
        api = self.apis["mikeapi"]
        endpoint, params, headers = api._requests["season"]
        params["year"] = str(year)
        rsp = self._request(url=api.base_url, endpoint=endpoint, token=api.token,
                            parameters=params, headers=headers)
        rsp_dict = json.loads(rsp)[0]
        """{
            "id": "dd12382e-1d9f-46ee-a5f7-c5104db28e43",
            "name": null,
            "year": 2024,
            "current": "1",
            "md5": "128ecb6b713a9e78607804e0a086eee2"
        }"""
        return {str(year): rsp_dict["id"]}