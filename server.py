from flask import Flask, render_template, request, redirect, url_for
import utils
from werkzeug.utils import secure_filename
import os
import data_manager


app = Flask(__name__)
app.config["IMAGE_UPLOADS"] = f"{os.getcwd()}/static/images"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPG", "PNG"]


@app.route("/", methods=["GET"])
def main_page():
    questions = data_manager.display_latest_questions()
    return render_template("index.html", questions=questions)


@app.route("/list", methods=["GET"])
def get_all_questions():
    questions = data_manager.get_questions()
    if request.args:
        order_by = request.args.get('order_by')
        order = request.args.get('order_direction')
        questions = data_manager.sort_questions(order_by, order)
    return render_template("index.html", questions=questions)


@app.route("/search", methods=["GET"])
def search_questions():
    sequence = request.args.get("sequence")
    questions = data_manager.search_question(sequence)
    return render_template("index.html", questions=questions)


@app.route("/question/<question_id>/increase_view")
def increase_view(question_id):
    data_manager.increase_view(question_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route("/question/<question_id>")
def display_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.answers_by_question_id(question_id)
    comments = data_manager.get_comments()
    return render_template("question.html", question=question[0], answers=answers, comments=comments)


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
        data_manager.add_question(question)
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
        data_manager.add_new_answer(answer)
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/delete", methods=["GET"])
def delete_question(question_id):
    if request.method == 'GET':
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
        data_manager.edit_question(question, question_id)

        return redirect(f"/question/{question_id}")
    return render_template("edit_question.html", question=question)


@app.route("/answer/<answer_id>/<question_id>/delete", methods=["GET"])
def delete_answer(answer_id, question_id):
    data_manager.delete_answer(answer_id)
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/new-comment", methods=["GET", "POST"])
def add_question_comment(question_id):
    if request.method == "POST":
        question_comment = dict()
        question_comment["message"] = request.form['comment']
        question_comment["edited_count"] = 0
        question_comment["question_id"] = question_id
        data_manager.add_new_question_comment(question_comment)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template("add_question_comment.html", question_id=question_id)


@app.route("/answer/<answer_id>/<question_id>/new-comment", methods=["GET", "POST"])
def add_answer_comment(answer_id, question_id):
    if request.method == "POST":
        answer_comment = dict()
        answer_comment["message"] = request.form["comment"]
        answer_comment['edited_count'] = 0
        answer_comment['answer_id'] = answer_id
        data_manager.add_answer_comment(answer_comment)
        return redirect(f"/question/{question_id}")
    return render_template("add_answer_comment.html", answer_id=answer_id, question_id=question_id)


@app.route("/question/<question_id>/vote_up", methods=["GET"])
def question_vote_up(question_id):
    data_manager.increase_vote_number("question", question_id)
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/vote_down", methods=["GET"])
def question_vote_down(question_id):
    data_manager.decrease_vote_number("question", question_id)
    return redirect(f"/question/{question_id}")


@app.route("/answer/<answer_id>/<question_id>/vote_up", methods=["GET"])
def answer_vote_up(answer_id, question_id):
    data_manager.increase_vote_number("answer", answer_id)
    return redirect(f"/question/{question_id}")


@app.route("/answer/<answer_id>/<question_id>/vote_down", methods=["GET"])
def answer_vote_down(answer_id, question_id):
    data_manager.decrease_vote_number("answer", answer_id)
    return redirect(f"/question/{question_id}")


@app.route("/comment/<comment_id>/<question_id>/edit", methods=["GET", "POST"])
def edit_comment(comment_id, question_id):
    comment = data_manager.get_comment_by_id(comment_id)[0]
    if request.method == "POST":
        comment["message"] = request.form.get("comment")
        data_manager.edit_comment(comment)
        return redirect(url_for("display_question", question_id=question_id))
    return render_template("edit_comment.html", comment=comment, question_id=question_id)


@app.route("/answer/<answer_id>/<question_id>/edit", methods=["GET", "POST"])
def edit_answer(answer_id, question_id):
    answer = utils.get_answers_by_question_id(answer_id)
    if request.method == "POST":
        answer['title'] = request.form['title']
        answer['message'] = request.form['message']
        if request.files:
            image = request.files["image"]
            if utils.allowed_image(image.filename, app.config["ALLOWED_IMAGE_EXTENSIONS"]):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                answer["image"] = f"images/{image.filename}"
        data_manager.edit_question(answer, answer_id)

        return redirect(f"/question/{question_id}")
    return render_template("edit_answer.html", answer=answer)


@app.route("/comments/<comment_id>/<question_id>delete")
def delete_comment(comment_id, question_id):
    data_manager.delete_comment(comment_id)
    return redirect(url_for('display_question', question_id=question_id))


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )
