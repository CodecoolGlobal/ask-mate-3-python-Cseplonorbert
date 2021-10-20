import csv
from date_handler import get_today_date_to_time_stamp

QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWERS_HEADERS = ['id','submission_time','vote_number','question_id','message','image']


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
    answers = get_data_from_file("answer.csv")
    new_id = len(answers)+1
    answer['id'] = new_id
    answer['vote_number'] = 0
    answer['submission_time'] = get_today_date_to_time_stamp()
    answers.append(answer)
    write_data_to_file(answers, ANSWERS_HEADERS, "answer.csv")


def delete_question_by_id(question_id):
    questions = get_data_from_file()
    for index, question in enumerate(questions):
        if question["id"] == question_id:
            delete_index = index
    del questions[delete_index]
    write_data_to_file(questions, QUESTION_HEADERS)


def edit_question(edited_question):
    questions = get_data_from_file()
    for question in questions:
        if question["id"] == edited_question["id"]:
            question["title"] = edited_question["title"]
            question["message"] = edited_question["message"]
            question["image"] = edited_question["image"]
    write_data_to_file(questions, QUESTION_HEADERS)


def delete_answer(answer_id):
    answers = get_data_from_file("answer.csv")
    for index, answer in enumerate(answers):
        if answer["id"] == answer_id:
            delete_index = index
    del answers[delete_index]
    write_data_to_file(answers, ANSWERS_HEADERS, "answer.csv")


def vote_question(question_id, vote):
    questions = get_data_from_file()
    for question in questions:
        if question["id"] == question_id:
            if vote == "up":
                question["vote_number"] = int(question["vote_number"]) + 1
            elif vote == "down":
                question["vote_number"] = int(question["vote_number"]) - 1
    write_data_to_file(questions, QUESTION_HEADERS)


def vote_answer(answer_id, vote):
    answers = get_data_from_file("answer.csv")
    for answer in answers:
        if answer["id"] == answer_id:
            if vote == "up":
                answer["vote_number"] = int(answer["vote_number"]) + 1
            elif vote == "down":
                answer["vote_number"] = int(answer["vote_number"]) - 1
    write_data_to_file(answers, ANSWERS_HEADERS, "answer.csv")
