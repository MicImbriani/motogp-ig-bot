from random import choice, randint

from src.collector import *



class ContentCreator():
    def __init__(self):
        self.collector = Collector()

    # pick n topics
    # if `evaluation=True`, allow user to confirm or discard
    def _pick_random_topics(self, amount=2, evaluation=False, verbose=True):
        years = [self.random_year() for i in range(amount)]
        if evaluation:
            timeout = 0
            topics_found = False
            while not topics_found and timeout < 15:
                topics = [choice(self.collector.topics) for i in range(amount)]
                x = input(f"{timeout}) The chosen topics are: `{topics}`.\nConfirm? (y/n)\n")
                topics_found = True if x=="y" else False
                timeout += 1
            if verbose:
                print("Topics chosen: " , topics)
                print("Years chosen: " , years)
            return topics, years
        else:
            topics = [choice(self.collector.topics) for i in range(amount)]
            if verbose:
                print("Topics chosen: " , topics)
                print("Years chosen: " , years)
            return topics, years

    def _generate_question(self, topics, years):
        content = dict.fromkeys(topics)
        for topic, year in zip(topics, years):
            content[topic] = self.collector.get_conent_from_topic(topic, year)
        # now that each topic has content, compose question and propose it to ChatGPT
        print("Generated Question: ")
        prompt = "I will give you two topics. You need to find some interesting facts about them.\n"
        for idx, topic in enumerate(list(content.keys())):
            prompt += f"\nTopic #{idx+1}: ({topic})\n{content[topic]}\n"
        return prompt

    def random_year(self, recent_bias=True):
        # year between 1949 and 2024
        y = randint(1949, 2024)
        return choice([y, 2024]) if recent_bias else y

    def send_question(self):
        topics, years = self._pick_random_topics()
        question = self._generate_question(topics, years)
        print(question)
    
    def season(self):
        self.collector.get_season_id(2024)
        