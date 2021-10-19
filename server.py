from flask import Flask, render_template
from bonus_questions import SAMPLE_QUESTIONS

app = Flask(__name__)


@app.route("/bonus-questions")
def main():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


@app.route("/question/<question_id>")
def display_question(question_id):
    question = data_handler.get_question_by_id(question_id)
    return render_template("question.html", question=question)


@app.route("/add_question", methods=["GET", "POST"])
def add_question():
    if request.method == "POST":
        question = dict()
        question['title'] = request.form['title']
        question['message'] = request.form['message']   
        data_handler.add_question(question)
        return redirect('/list')
    elif request.method == "GET":
        return render_template("add_question.html")


@app.route("/question/<question_id>/new_answer", methods=["POST"])
def add_new_answer(question_id):
    if request.method == "POST":
        answer = request.form
        answer["answer_id"]=question_id
        data_handler.add_new_answer(answer)
    return redirect("/question/<question_id>")


@app.route("/question/<question_id>/delete", methods=["GET"])
def delete_question(question_id):
    if request.method == 'GET':
        data_handler.delete_question_by_id(question_id)
        return redirect('/list')


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    question = data_handler.get_question_by_id(question_id)
    if request.method == "POST":
        question = request.form
        data_handler.edit_question(question)
        return redirect("/question/<question_id>")
    return render_template("edit_question.html", question=question)


@app.route("/answer/<answer_id>/delete", methods = ["GET"])
def delete_answer(answer_id):
    data_handler.delete_answer(answer_id)
    return redirect("/question/<question_id>")


@app.route("/question/<question_id>/vote_up", methods=["GET"])
def question_vote_up(question_id):
    data_handler.vote_up_question(question_id)
    return redirect("/question/<question_id>")


@app.route("/question/<question_id>/vote_down", methods=["GET"])
def question_vote_down(question_id):
    data_handler.vote_down_question(question_id)
    return redirect("/question/<question_id>")


@app.route("/answer/<answer_id>/vote_up", methods=["GET"])
def answer_vote_up(answer_id):
    data_handler.vote_up_answer(answer_id)
    return redirect("/question/<question_id>")


@app.route("/answer/<answer_id>/vote_down", methods=["GET"])
def answer_vote_down(answer_id):
    data_handler.vote_down_answer(answer_id)
    return redirect("/question/<question_id>")


if __name__ == "__main__":
    app.run(debug=True)
