import csv
from datetime import date, datetime

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
    post_date = datetime.fromtimestamp(submission_time)
    return post_date


def write_questions_to_file(questions, file_name="question.csv"):
    with open(file_name, "w+") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(questions)


def get_question_by_id(question_id):
    pass


def date_time_to_timestamp(date_time):
    submission_time = datetime.timestamp(date_time)
    return submission_time


def add_question(question):
    questions = get_questions()
    new_id = len(questions)+1
    question['id'] = new_id
    question['view_number'] = 0
    question['vote_number'] = 0
    today_date = datetime.now()
    question['submission_time'] = date_time_to_timestamp(today_date)
    questions.append(question)
    write_questions_to_file(questions)

    
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
