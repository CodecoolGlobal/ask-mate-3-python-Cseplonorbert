import csv
from date_handler import get_today_date_to_time_stamp

HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]


def get_questions(file_name="question.csv"):
    with open(file_name, "r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        questions = list(reader)
        return questions


def write_questions_to_file(questions, file_name="question.csv"):
    with open(file_name, "w+") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(questions)


def get_question_by_id(question_id):
    pass


def add_question(question):
    questions = get_questions()
    new_id = len(questions)+1
    question['id'] = new_id
    question['view_number'] = 0
    question['vote_number'] = 0
    question['submission_time'] = get_today_date_to_time_stamp()
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
