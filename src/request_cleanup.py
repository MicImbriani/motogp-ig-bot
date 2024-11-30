news_delete = [
    "title",
    "link",
    "pubDate",
    "imageURL",
    "category"
]

riders_delete = [
    "md5",
    "classification_id",
]

results_delete = [
    "md5",
    "classification_id",
]



dict = {
    "news": news_delete,
    "riders": riders_delete,
}

def rsp_cleanup(topic, content):
    # print("MIC ", content)
    # print("MIC TYPE :", type(content))
    # print()
    
    # raw =  {'md5': '6eb89710845db587f6f4babd725e45ff', 'classification_id': '3ffcc9fb-bf03-4d5a-991e-99f6948b1ae0', 'constructor_name': 'Yamaha', 'rider_country_iso': 'FR', 'rider_full_name': 'Fabio Quartararo', 'year': '2021', 'points': 278, 'position': 1, 'team_color': '#0c368c', 'text_color': '#ffffff'},
    # edit = {'constructor_name': 'Yamaha', 'rider_country_iso': 'FR', 'rider_full_name': 'Fabio Quartararo', 'year': '2021', 'points': 278, 'position': 1, 'team_color': '#0c368c', 'text_color': '#ffffff'},
    if topic == "riders":
        new_content = []
        for rider_entry in content:
            del rider_entry['md5']
            del rider_entry['classification_id']
            new_content.append(rider_entry)
    
    elif type(content) == list:
        # print("LEN LIST :", len(content))
        new_content = content[0]
    # print("CONTENT ", content)
    # print("CONTENT TYPE :", type(content))
    # for i in dict[topic]:
    #     del content[i]

    print("CLEAN CONTENT ", new_content)
    return new_content
