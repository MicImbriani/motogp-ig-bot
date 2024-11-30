from random import choice, randint

from src.collector import *
from .request_cleanup import rsp_cleanup



class ContentCreator():
    def __init__(self, eval):
        self.collector = Collector()
        self.evaluate_topics = eval         # allow user to confirm or discard

    # pick n topics
    def _pick_random_topics(self, amount=2):
        if self.evaluate_topics:
            timeout = 0
            topics_found = False
            while not topics_found and timeout < 15:
                topics = [choice(self.collector.topics) for i in range(amount)]
                x = input(f"{timeout}) The chosen topics are: `{topics}`.\nConfirm? (y/n)\n")
                topics_found = True if x=="y" else False
                timeout += 1
        else:
            #{'topic_0': ['events', 1999], 'topic_1': ['events', 2024]}
            topics = {}
            for i in range(amount):
                topics[f'topic_{i}'] = [str(choice(self.collector.topics)),
                                        self.random_year()]

        return topics


    def _generate_question(self, topics):
        # topics: {'topic_0': ['events', 1999], 'topic_1': ['events', 2024]}
        content = dict.fromkeys(list(topics.keys()))
        for topic_N, val in topics.items():
            topic, year = val
            gtp_rsp = self.collector.get_conent_from_topic(topic, year)
            if topic != "calendar" and topic != "news" and topic != "events":
                clean_gpt_rsp = rsp_cleanup(topic, json.loads(gtp_rsp))
                content[topic_N] = clean_gpt_rsp
            else:
                content[topic_N] = gtp_rsp

        # prompt = prompt if not clean_output else rsp_cleanup(topics, question)
        # now that each topic has content, compose question and propose it to ChatGPT
        prompt = "I will give you two topics. You need to find some interesting in-depth facts, and relationships about them that are not obvious to the naked eye.\n"
        # print("content: ", content)
        for idx, topic_N in enumerate(list(content.keys())):
            prompt += f"\nTopic #{idx}: ({topics[topic_N][0]} - {topics[topic_N][1]})\n{content[topic_N]}\n"
        return prompt

    def random_year(self, recent_bias=True):
        # year between 1949 and 2024
        y = randint(1990, 2024)
        return choice([y, 2024]) if recent_bias else y

    def get_question(self, clean_output=True, verbose=True):
        topics = self._pick_random_topics()
        if verbose:
            print("Topics chosen: " , topics)
        question = self._generate_question(topics)
        return question

    def season(self):
        self.collector.get_season_id(2024)
