from random import choice

from collector import *



class ContentCreator():
    def __init__(self):
        self.collector = Collector()

    # pick n topics
    # if `evaluation=True`, allow user to confirm or discard
    def _pick_random_topics(self, amount=2, evaluation=False, verbose=True):
        if evaluation:
            timeout = 0
            topics_found = False
            while not topics_found and timeout < 15:
                topics = [choice(self.collector.topics) for i in range(amount)]
                x = input(f"{timeout}) The chosen topics are: `{topics}`.\nConfirm? (y/n)\n")
                topics_found = True if x=="y" else False
                timeout += 1
            if verbose: print("Topics chosen: " , topics)
            return topics
        else:
            topics = [choice(self.collector.topics) for i in range(amount)]
            if verbose: print("Topics chosen: " , topics)
            return topics

    def _generate_question(self, topics):
        content = dict.fromkeys(topics)
        for topic in topics:
            content[topic] = self.collector.get_conent_from_topic(topic)
        # now that each topic has content, compose question and propose it to ChatGPT
        print("Generated Question: ")
        prompt = "I will give you two topics. You need to find some interesting facts about them.\n"
        for idx, topic in enumerate(list(content.keys())):
            prompt += f"\nTopic #{idx+1}: ({topic})\n{content[topic]}\n"
        return prompt

    def send_question(self):
        question = self._generate_question(self._pick_random_topics())
        print(question)
    