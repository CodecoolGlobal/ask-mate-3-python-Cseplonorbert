from datetime import datetime
from connection import get_data_from_file


def get_string_date_by_timestamp(timestamp):
    timestamp = int(timestamp)
    dt_object = datetime.fromtimestamp(timestamp)
    date_time = dt_object.strftime("%m/%d/%Y, %H:%M")
    return date_time


def get_today_date_to_time_stamp():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return int(timestamp)


def convert_timestamps_to_date(data):
    for dictionary in data:
        timestamp = dictionary["submission_time"]
        dictionary["submission_time"] = get_string_date_by_timestamp(timestamp)
    return data


def sort_questions(questions, order_by, order):
    if (order_by == "view_number" or order_by == "vote_number") and order == "ascend":
        questions = sorted(questions, key=lambda k: int(k[order_by]))
    elif (order_by == "view_number" or order_by == "vote_number") and order == "desc":
        questions = sorted(questions, key=lambda k: int(k[order_by]), reverse=True)
    elif order == "ascend":
        questions = sorted(questions, key=lambda k: k[order_by])
    elif order == "desc":
        questions = sorted(questions, key=lambda k: k[order_by], reverse=True)
    return questions


def get_question_by_id(question_id):
    questions = get_data_from_file()
    for question in questions:
        if question['id'] == question_id:
            return question


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


def allowed_image(filename, allowed_extensions):
    if "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in allowed_extensions:
        return True
    else:
        return False
