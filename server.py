from flask import Flask, render_template, request, redirect
import data_handler
import utils
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config["IMAGE_UPLOADS"] = f"{os.getcwd()}/static/images"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPG", "PNG"]


@app.route("/", methods=["GET"])
@app.route("/list", methods=["GET"])
def main_page():
    questions = data_handler.get_data_from_file()
    questions = utils.convert_timestamps_to_date(questions)
    if request.args:
        order_by = request.args.get('order_by')
        order = request.args.get("order")
        questions = utils.sort_questions(questions, order_by, order)
    return render_template("index.html", questions=questions)


@app.route("/question/<question_id>")
def display_question(question_id):
    data_handler.increase_view(question_id)
    question = utils.get_question_by_id(question_id)
    answers = utils.get_answers_by_question_id(question_id)
    answers = utils.convert_timestamps_to_date(answers)
    return render_template("question.html", question=question, answers=answers)


@app.route("/add_question", methods=["GET", "POST"])
def add_question():
    if request.method == "POST":
        question = dict()
        if request.files:
            image = request.files["image"]
            if utils.allowed_image(image.filename, app.config["ALLOWED_IMAGE_EXTENSIONS"]):
                filename = secure_filename(image.filename)

                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                question["image"] = f"images/{image.filename}"

        question['title'] = request.form['title']
        question['message'] = request.form['message']
        data_handler.add_question(question)
        return redirect('/list')
    elif request.method == "GET":
        return render_template("add_question.html")


@app.route("/question/<question_id>/new_answer", methods=["POST"])
def add_new_answer(question_id):
    answer = dict()
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            if utils.allowed_image(image.filename, app.config["ALLOWED_IMAGE_EXTENSIONS"]):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                answer["image"] = f"images/{image.filename}"
        answer["message"] = request.form["message"]
        answer["question_id"] = question_id
        data_handler.add_new_answer(answer)
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/delete", methods=["GET"])
def delete_question(question_id):
    if request.method == 'GET':
        answers = utils.get_answers_by_question_id(question_id)
        if answers:
            for answer in answers:
                answer_id = answer['id']
                data_handler.delete_by_id(answer_id, 'answer')
        data_handler.delete_by_id(question_id, "question")
        data_manager.delete_question_id(question_id)
        return redirect('/list')


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    question = utils.get_question_by_id(question_id)
    if request.method == "POST":
        question['title'] = request.form['title']
        question['message'] = request.form['message']
        if request.files:
            image = request.files["image"]
            if utils.allowed_image(image.filename, app.config["ALLOWED_IMAGE_EXTENSIONS"]):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                question["image"] = f"images/{image.filename}"
        data_handler.edit_question(question)

        return redirect(f"/question/{question_id}")
    return render_template("edit_question.html", question=question)


@app.route("/answer/<answer_id>/delete", methods=["GET"])
def delete_answer(answer_id):
    question_id = utils.get_question_id_by_answer_id(answer_id)
    data_handler.delete_by_id(answer_id, "answer")
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/new-comment", methods=["GET", "POST"])
def add_question_comment(question_id):
    return render_template("add_question_comment.html")


@app.route("/answer/<answer_id>/new-comment", methods=["GET", "POST"])
def add_answer_comment(question_id, answer_id):
    if request.method == "POST":
        answer_comment = request.form['answer_comment']
        answer_comment['edit_count'] = 0
        data_manager.add_answer_comment(answer_comment, question_id, answer_id)
        return redirect(f"/question/{question_id}")
    return render_template("add_answer_comment.html", answer_id=answer_id, question_id=question_id)


@app.route("/question/<question_id>/vote_up", methods=["GET"])
def question_vote_up(question_id):
    data_handler.vote_dict(question_id, "up", "question")
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/vote_down", methods=["GET"])
def question_vote_down(question_id):
    data_handler.vote_dict(question_id, "down", "question")
    return redirect(f"/question/{question_id}")


@app.route("/answer/<answer_id>/vote_up", methods=["GET"])
def answer_vote_up(answer_id):
    question_id = utils.get_question_id_by_answer_id(answer_id)
    data_handler.vote_dict(answer_id, "up", "answer")
    return redirect(f"/question/{question_id}")


@app.route("/answer/<answer_id>/vote_down", methods=["GET"])
def answer_vote_down(answer_id):
    question_id = utils.get_question_id_by_answer_id(answer_id)
    data_handler.vote_dict(answer_id, "down", "answer")
    return redirect(f"/question/{question_id}")


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )
