from random import choice, randint

from src.collector import *
from .request_cleanup import rsp_cleanup



class ContentCreator():
    def __init__(self):
        self.collector = Collector()

    # pick n topics
    # if `evaluation=True`, allow user to confirm or discard
    def _pick_random_topics(self, amount=2, evaluation=False,):
        years = [self.random_year() for i in range(amount)]
        if evaluation:
            timeout = 0
            topics_found = False
            while not topics_found and timeout < 15:
                topics = [choice(self.collector.topics) for i in range(amount)]
                x = input(f"{timeout}) The chosen topics are: `{topics}`.\nConfirm? (y/n)\n")
                topics_found = True if x=="y" else False
                timeout += 1
        else:
            topics = [choice(self.collector.topics) for i in range(amount)]

        return topics, years


    def _generate_question(self, topics, years, clean_output=True):
        content = dict.fromkeys(topics)
        for topic, year in zip(topics, years):
            gtp_rsp = self.collector.get_conent_from_topic(topic, year)
            if topic != "calendar" and topic != "news" and topic != "events":
                clean_gpt_rsp = rsp_cleanup(topic, json.loads(gtp_rsp))
                content[topic] = clean_gpt_rsp
            else:
                content[topic] = gtp_rsp

        # prompt = prompt if not clean_output else rsp_cleanup(topics, question)
        # now that each topic has content, compose question and propose it to ChatGPT
        prompt = "I will give you two topics. You need to find some interesting in-depth facts, and relationships about them that are not obvious to the naked eye.\n"
        for idx, topic in enumerate(list(content.keys())):
            prompt += f"\nTopic #{idx+1}: ({topic})\n{content[topic]}\n"
        return prompt

    def random_year(self, recent_bias=True):
        # year between 1949 and 2024
        y = randint(1990, 2024)
        return choice([y, 2024]) if recent_bias else y

    def get_question(self, clean_output=True, verbose=True):
        topics, years = self._pick_random_topics()
        if verbose:
            print("Topics chosen: " , topics)
            print("Years chosen: " , years)
        question = self._generate_question(topics, years)
        return question

    def season(self):
        self.collector.get_season_id(2024)
