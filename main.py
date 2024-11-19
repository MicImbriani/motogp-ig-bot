from src.contentCreator import ContentCreator
import datetime;



rsp_save_dir = "/home/mic/coding/motogp-ig-bot/data/"

def get_time_stamp():
    ct = datetime.datetime.now()
    return str(ct).replace(" ", "_")[:-7]

def export_to_txt(content, file_name=get_time_stamp()+".txt"):
    with open(rsp_save_dir+file_name, "w") as f:
        f.write(content)

if __name__ == '__main__':
    content_creator = ContentCreator()
    question = content_creator.get_question()
    export_to_txt(question)