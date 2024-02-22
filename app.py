from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses =[]

@app.get("/")
def serve_home_page():
    return render_template('survey_start.html')

@app.post('/begin')
def serve_questions():

    return redirect('/questions/0')

@app.get('/questions/0')
def first_question():

    question = survey.questions[0]

    return render_template('question.html', question = question)
