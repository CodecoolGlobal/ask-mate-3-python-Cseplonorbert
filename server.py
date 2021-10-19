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


if __name__ == "__main__":
    app.run(debug=True)
