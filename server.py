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


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == "POST":
        question = request.form
        data_handler.add_question(question)
        return redirect('/list')
    elif request.method == "GET":
        return render_template("add_question.html")


@app.route("/question/<question_id>/new_answer", methods =["POST"])
def add_new_answer(question_id):
    if request.method == "POST":
        answer = request.form
        answer["answer_id"]=question_id
        data_handler.add_new_answer(answer)
    return redirect("/question/<question_id>")


if __name__ == "__main__":
    app.run(debug=True)
