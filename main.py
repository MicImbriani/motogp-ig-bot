import datetime
import argparse

from src.contentCreator import ContentCreator



rsp_save_dir = "/home/mic/coding/motogp-ig-bot/data/"

parser = argparse.ArgumentParser()
parser.add_argument('--eval', dest='eval', action='store_true', help="Receive prompt to evaluate and confirm/discard the chosen topics.")
args = parser.parse_args()


def get_time_stamp():
    ct = datetime.datetime.now()
    return str(ct).replace(" ", "_")[:-7]

def export_to_txt(content, file_name=get_time_stamp()+".txt"):
    with open(rsp_save_dir+file_name, "w") as f:
        f.write(content)

if __name__ == '__main__':
    content_creator = ContentCreator(args.eval)
    question = content_creator.get_question()
    export_to_txt(question)