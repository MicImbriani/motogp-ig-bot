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
    print("MIC ", content)
    print("MIC TYPE :", type(content))
    if type(content) == list:
        print("LEN LIST :", len(content))
        content = content[0]
    print("CONTENT ", content)
    print("CONTENT TYPE :", type(content))
    for i in dict[topic]:
        del content[i]

    print("CLEAN CONTENT ", content)
    return content
