import csv
from date_handler import get_today_date_to_time_stamp
import os

QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWERS_HEADERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_data_from_file(file_name="question.csv"):
    with open(file_name, "r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        data = list(reader)
        return data


def write_data_to_file(data, headers, file_name="question.csv"):
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
    questions.append(question)
    write_data_to_file(questions, QUESTION_HEADERS)


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
    answers = get_data_from_file("answer.csv")
    new_id = len(answers)+1
    answer['id'] = new_id
    answer['vote_number'] = 0
    answer['submission_time'] = get_today_date_to_time_stamp()
    answers.append(answer)
    write_data_to_file(answers, ANSWERS_HEADERS, "answer.csv")


def get_file_name_and_headers_by_type(datatype):
    if datatype == "question":
        file_name = "question.csv"
        headers = QUESTION_HEADERS
    else:
        file_name = "answer.csv"
        headers = ANSWERS_HEADERS
    return file_name, headers


def delete_by_id(dictionary_id, datatype):
    delete_index = False
    file_name, headers = get_file_name_and_headers_by_type(datatype)
    file_data = get_data_from_file(file_name)
    for index, dictionary in enumerate(file_data):
        if dictionary["id"] == dictionary_id:
            delete_index = index
    if delete_index:
        if file_data[delete_index]['image']:
            os.remove(f"./static/{file_data[delete_index]['image']}")
        del file_data[delete_index]
        write_data_to_file(file_data, headers, file_name)


def edit_question(edited_question):
    questions = get_data_from_file()
    for question in questions:
        if question["id"] == edited_question["id"]:
            question["title"] = edited_question["title"]
            question["message"] = edited_question["message"]
            if edited_question["image"]:
                if question["image"]:
                    os.remove(f"./static/{question['image']}")
                question["image"] = edited_question["image"]
    write_data_to_file(questions, QUESTION_HEADERS)


def vote_dict(dictionary_id, vote, datatype):
    file_name, headers = get_file_name_and_headers_by_type(datatype)
    file_data = get_data_from_file(file_name)
    for dictionary in file_data:
        if dictionary["id"] == dictionary_id:
            if vote == "up":
                dictionary["vote_number"] = int(dictionary["vote_number"]) + 1
            elif vote == "down":
                dictionary["vote_number"] = int(dictionary["vote_number"]) - 1
    write_data_to_file(file_data, headers, file_name)


def increase_view(question_id):
    questions = get_data_from_file()
    for question in questions:
        if question['id'] == question_id:
            question['view_number'] = int(question['view_number']) + 1
    write_data_to_file(questions, QUESTION_HEADERS)


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
