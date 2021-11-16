from flask import Flask, session, render_template, request, redirect, url_for,flash
import utils
from werkzeug.utils import secure_filename
import os
import data_manager

app = Flask(__name__)
app.config["IMAGE_UPLOADS"] = f"{os.getcwd()}/static/images"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPG", "PNG"]
app.secret_key = '12345abc'


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
    return render_template("question.html", question=question, answers=answers, comments=comments)


@app.route("/add_question", methods=["GET", "POST"])
def add_question():
    if 'email' in session:
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
            question['user_id'] = session['user_id']
            data_manager.add_question(question)
            return redirect('/list')
        elif request.method == "GET":
            return render_template("add_question.html")
    else:
        return redirect(url_for('main_page'))


@app.route("/question/<question_id>/new_answer", methods=["POST"])
def add_new_answer(question_id):
    if 'email' in session:
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
            answer["user_id"] = session["user_id"]
            data_manager.add_new_answer(answer)
            return redirect(url_for('display_question', question_id=question_id))
    else:
        return redirect(url_for('display_question', question_id=question_id))


@app.route("/question/<question_id>/delete", methods=["GET"])
def delete_question(question_id):
    if 'email' in session:
        question = data_manager.get_question_by_id(question_id)
        if session['user_id'] == question['user_id']:
            data_manager.delete_question_id(question_id)
            return redirect(url_for('main_page'))
        else:
            return redirect(url_for('display_question', question_id=question_id))
    else:
        return redirect(url_for('display_question', question_id=question_id))


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    if 'email' in session:
        question = data_manager.get_question_by_id(question_id)
        if session['user_id'] == question['user_id']:
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

                return redirect(url_for('display_question', question_id=question_id))
            return render_template("edit_question.html", question=question)
        else:
            return redirect(url_for('display_question', question_id=question_id))
    else:
        return redirect(url_for('display_question', question_id=question_id))


@app.route("/answer/<answer_id>/<question_id>/delete", methods=["GET"])
def delete_answer(answer_id, question_id):
    if 'email' in session:
        answer = data_manager.get_answer_by_id(answer_id)
        if answer['user_id'] == session['user_id']:
            data_manager.delete_answer(answer_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route("/question/<question_id>/new-comment", methods=["GET", "POST"])
def add_question_comment(question_id):
    if 'email' in session:
        if request.method == "POST":
            question_comment = dict()
            question_comment["message"] = request.form['comment']
            question_comment["edited_count"] = 0
            question_comment["question_id"] = question_id
            question_comment["user_id"] = session['user_id']
            data_manager.add_new_question_comment(question_comment)
            return redirect(url_for('display_question', question_id=question_id))
        return render_template("add_question_comment.html", question_id=question_id)
    else:
        return redirect(url_for('display_question', question_id=question_id))


@app.route("/answer/<answer_id>/<question_id>/new-comment", methods=["GET", "POST"])
def add_answer_comment(answer_id, question_id):
    if 'email' in session:
        if request.method == "POST":
            answer_comment = dict()
            answer_comment["message"] = request.form["comment"]
            answer_comment['edited_count'] = 0
            answer_comment['answer_id'] = answer_id
            answer_comment['user_id'] = session['user_id']
            data_manager.add_answer_comment(answer_comment)
            return redirect(url_for('display_question', question_id=question_id))
        return render_template("add_answer_comment.html", answer_id=answer_id, question_id=question_id)
    else:
        return redirect(url_for('display_question', question_id=question_id))


@app.route("/question/<question_id>/vote_up", methods=["GET"])
def question_vote_up(question_id):
    if 'email' in session:
        question = data_manager.get_question_by_id(question_id)
        if session['user_id'] != question['user_id']:
            data_manager.increase_vote_number("question", question_id)
            return redirect(url_for('display_question', question_id=question_id))
        else:
            return redirect(url_for('display_question', question_id=question_id))
    else:
        return redirect(url_for('display_question', question_id=question_id))


@app.route("/question/<question_id>/vote_down", methods=["GET"])
def question_vote_down(question_id):
    if 'email' in session:
        question = data_manager.get_question_by_id(question_id)
        if session['user_id'] != question['user_id']:
            data_manager.decrease_vote_number("question", question_id)
            return redirect(url_for('display_question', question_id=question_id))
        else:
            return redirect(url_for('display_question', question_id=question_id))
    else:
        return redirect(url_for('display_question', question_id=question_id))


@app.route("/answer/<answer_id>/<question_id>/vote_up", methods=["GET"])
def answer_vote_up(answer_id, question_id):
    if 'email' in session:
        answer = data_manager.get_answer_by_id(answer_id)
        if answer['user_id'] != session['user_id']:
            data_manager.increase_vote_number("answer", answer_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route("/answer/<answer_id>/<question_id>/vote_down", methods=["GET"])
def answer_vote_down(answer_id, question_id):
    if 'email' in session:
        answer = data_manager.get_answer_by_id(answer_id)
        if answer['user_id'] != session['user_id']:
            data_manager.decrease_vote_number("answer", answer_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route("/comment/<comment_id>/<question_id>/edit", methods=["GET", "POST"])
def edit_comment(comment_id, question_id):
    comment = data_manager.get_comment_by_id(comment_id)
    if 'email' in session:
        if session['user_id'] == comment['user_id']:
            if request.method == "POST":
                comment["message"] = request.form.get("comment")
                data_manager.edit_comment(comment)
            else:
                return render_template("edit_comment.html", comment=comment, question_id=question_id)
    return redirect(url_for("display_question", question_id=question_id))


@app.route("/answer/<answer_id>/<question_id>/edit", methods=["GET", "POST"])
def edit_answer(answer_id, question_id):
    if 'email' in session:
        answer = data_manager.get_answer_by_id(answer_id)
        if session['user_id'] == answer['user_id']:
            if request.method == "POST":
                answer['message'] = request.form['message']
                if request.files:
                    image = request.files["image"]
                    if utils.allowed_image(image.filename, app.config["ALLOWED_IMAGE_EXTENSIONS"]):
                        filename = secure_filename(image.filename)
                        image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                        answer["image"] = f"images/{image.filename}"
                data_manager.edit_answer(answer, answer_id)
                return redirect(url_for('display_question', question_id=question_id))
            else:
                return render_template("edit_answer.html", answer=answer)
        else:
            return redirect(url_for('display_question', question_id=question_id))
    else:
        return redirect(url_for('display_question', question_id=question_id))


@app.route("/comments/<comment_id>/<question_id>delete")
def delete_comment(comment_id, question_id):
    if 'email' in session:
        comment = data_manager.get_comment_by_id(comment_id)
        if comment['user_id'] == session['user_id']:
            data_manager.delete_comment(comment_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route("/user/<user_id>")
def get_user_page(user_id):
    if 'email' in session:
        user_data = data_manager.get_user_data(user_id)
        related_answers = data_manager.get_related_answers(user_id)
        related_questions = data_manager.get_related_questions(user_id)
        related_comments = data_manager.get_related_comments(user_id)
        number_of_related_answers = data_manager.count_related_answers(user_id)
        number_of_related_questions = data_manager.count_related_questions(user_id)
        number_of_related_comments = data_manager.count_related_comments(user_id)
        return render_template('user_page.html', user_data=user_data,
                               related_answers=related_answers,
                               related_questions=related_questions,
                               related_comments=related_comments,
                               number_of_related_comments=number_of_related_comments,
                               number_of_related_answers=number_of_related_answers,
                               number_of_related_questions=number_of_related_questions)
    else:
        return redirect(url_for('main_page'))


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user_info = data_manager.get_user_info(email)
        if not user_info:
            flash("Invalid username or password ")
            return redirect(url_for('login_page'))
        else:
            verified_password = utils.verify_password(password, user_info[0]['password'])
            if not verified_password:
                flash("Invalid username/password combination")
                return redirect(url_for('login_page'))
            else:
                session['user_id'] = user_info[0]['id']
                session['email'] = user_info[0]['email']
                return redirect(url_for('main_page'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id')
    session.pop('email', None)
    return redirect(url_for('main_page'))


@app.route("/registration", methods=['GET', 'POST'])
def registrate():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password_hashed = utils.hash_password(password)
        data_manager.registrate_user(email, password_hashed)
        return redirect("/")
    elif request.method == 'GET':
        return render_template('registration.html')


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )
