from utils import get_today_date_to_time_stamp
from connection import get_data_from_file, write_data_to_file
import os

QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWERS_HEADERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_id(datatype):
    file_name, headers = get_file_name_and_headers_by_type(datatype)
    file_data = get_data_from_file(file_name)
    last_dictionary = file_data[-1]
    last_dictionary_id = int(last_dictionary['id'])
    new_id = last_dictionary_id + 1
    return new_id


def add_question(question):
    questions = get_data_from_file()
    new_id = get_id("question")
    question['id'] = new_id
    question['view_number'] = 0
    question['vote_number'] = 0
    question['submission_time'] = get_today_date_to_time_stamp()
    questions.append(question)
    write_data_to_file(questions, QUESTION_HEADERS)


def add_new_answer(answer):
    answers = get_data_from_file("answer.csv")
    new_id = get_id("answer")
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
