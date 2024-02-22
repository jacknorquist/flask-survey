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

@app.get('/questions/<new_question>')
def first_question(new_question):

    question = survey.questions[int(new_question)]


    return render_template('question.html', question = question)

@app.post('/answer')
def get_response():
    responses.append(request.form.get('answer'))
    if len(responses) >= len(survey.questions):
        return redirect('/thankyou')
    else:
        question = str(len(responses))


        return redirect(f'/questions/{question}')

@app.get('/thankyou')
def get_thank_you_message():

    return render_template('completion.html')