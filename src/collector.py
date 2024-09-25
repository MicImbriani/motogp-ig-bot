import requests
import json

from api_keys import *      # <- gitignored. Contains personal API keys


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
                            {}],    # motogp, moto2, moto3, motoE
            "categories":   ["motogp-category",
                             {"year": "2024"},
                             {}],
            "season":       ["motogp-season",
                             {"year": "2024"},
                             {}],
            "events":       ["motogp-events",
                             {"year": "2024"},
                             {}],
            "sprint-race":  ["motogp-sessions-spr",
                             {"year": "2024"},
                             {}],
            "results":      ["motogp-full-results",
                             {"eventid": "8ed52491-e1aa-49a9-8d70-f1c1f8dd3090",
                              "year": "2024",
                              "session": "af960ae0-845e-4fac-a431-4a7ea6c7d128"},
                             {}],    # RAC FP1 FP2 FP3 FP4 Q1 Q2 WUP SPR
            "calendar":     ["motogp-calendar",
                             {"filter": "upcoming"},
                             {}]      # upcoming or full
        }
    
    @property
    def topics(self):
        return list(self.requests.keys())



class RapidAPI():
    def __init__(self):
        self.name = "RapidAPI"
        self.base_url = "https://motogp-news.p.rapidapi.com/motogpnews"
        self.token = "36365c3e79msha845393c2dbbf94p168759jsn016976429d16"

        # {topic:   endpoint,
        #           params,
        #           headers}
        self.requests = {
            "news":         ["motogpnews/0/0",
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

    # generic function for sending API requests
    def _request(self, url, endpoint, parameters=None, headers=None):
        response = requests.get(url + endpoint,
                                params=parameters,
                                headers=headers)

        json_response = response.json()
        json_formatted_str = json.dumps(json_response, indent=2)
        return json_formatted_str

    # given topic, retrieve the parameters and get content
    def get_conent_from_topic(self, topic):
        api = self._find_api_from_topic(topic)
        print("AAA ", api.name)
        endpoint, params, headers = api.requests[topic]
        return self._request(url=api.base_url, endpoint=endpoint, parameters=params, headers=headers)