import requests
import json

api_url = "https://api.micheleberardi.com/racing/v1.0/"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"

base_requests = {
    "rider":        ["motogp-world-standing-riders",
                        {"token": token,
                         "year": "2024",
                         "categoryid": "e8c110ad-64aa-4e8e-8a86-f2f152f6a942"}],    # motogp, moto2, moto3, motoE
    "categories":   ["motogp-category",
                        {"token": token,
                         "year": "2024"}],
    "season":       ["motogp-season",
                        {"token": token,
                         "year": "2024"}],
    "events":       ["motogp-events",
                        {"token": token,
                         "year": "2024"}],
    "sprint-race":  ["motogp-sessions-spr",
                        {"token": token,
                         "year": "2024"}],
    "results":      ["motogp-full-results",
                        {"token": token,
                         "eventid": "8ed52491-e1aa-49a9-8d70-f1c1f8dd3090",
                         "year": "2024",
                         "session": "af960ae0-845e-4fac-a431-4a7ea6c7d128"}],    # RAC FP1 FP2 FP3 FP4 Q1 Q2 WUP SPR
    "calendar":     ["motogp-calendar",
                        {"token": token,
                         "filter": "upcoming"}]      # upcoming or full
}

def _request(endpoint, parameters):
    response = requests.get(api_url + endpoint, 
                            params=parameters)

    json_response = response.json()
    json_formatted_str = json.dumps(json_response, indent=2)
    return json_formatted_str
