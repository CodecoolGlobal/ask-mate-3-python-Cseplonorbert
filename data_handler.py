import csv
from date_handler import get_today_date_to_time_stamp

QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWERS_HEADERS = ['id','submission_time','vote_number','question_id','message','image']

def get_data_from_file(file_name="question.csv"):
    with open(file_name, "r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        data = list(reader)
        return data


def write_data_to_file(data,headers, file_name="question.csv"):
    with open(file_name, "w+") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


def get_question_by_id(question_id):
    questions = get_data_from_file()
    for question in questions:
        if question['id'] == question_id:
            return question



def add_question(question):
    questions = get_data_from_file()
    new_id = len(questions)+1
    question['id'] = new_id
    question['view_number'] = 0
    question['vote_number'] = 0
    question['submission_time'] = get_today_date_to_time_stamp()
    questions.append()
    write_data_to_file(questions,QUESTION_HEADERS)


def get_answers_by_question_id(question_id):
    answers = get_data_from_file('answer.csv')
    related_answers = []
    for answer in answers:
        if answer['question_id'] == question_id:
            related_answers.append(answer)
    return related_answers


def get_question_id_by_answer_id(answer_id):
    answers = get_data_from_file("answer.csv")
    for answer in answers:
        if answer['id'] == answer_id:
            question_id = answer["question_id"]
    return question_id


def add_new_answer(answer):
    pass


def delete_question_by_id(question_id):
    pass


def edit_question(question):
    pass


def delete_answer(answer_id):
    pass


def vote_up_question(question_id):
    pass


def vote_down_question(question_id):
    pass


def vote_up_answer(answer_id):
    pass


def vote_down_answer(answer_id):
    pass
