import csv
from datetime import date

HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]


def get_questions(file_name="question.csv"):
    with open(file_name, "r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        questions = list(reader)
        questions = convert_dates(questions)
        return questions


def convert_dates(questions):
    for question in questions:
        submission_time = question["submission_time"]
        question["submission_time"] = get_date(int(submission_time))
    return questions


def get_date(submission_time):
    post_date = date.fromtimestamp(submission_time)
    return post_date


def write_questions_to_file(file_name="question.csv"):
    pass


def get_question_by_id(question_id):
    pass


def add_question(question):
    pass


def get_answers(file_name = "answers.csv"):
    pass


def write_answers_to_file(file_name = "answers.csv"):
    pass


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
