from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)



@app.get("/")
def serve_home_page():
    """Clears the session[“session["responses"]”] list and starts the survey"""
    session["responses"] =[]
    return render_template('survey_start.html', survey = survey)

@app.post('/begin')
def start_survey():
    """Redirects to the first question"""
    session["responses"].clear()
    return redirect('/questions/0')

@app.get('/questions/<int:question_id>')
def first_question(question_id):
    """Shows the question and gives choices."""

    if question_id > len(session["responses"]):
        flash("Please answer the previous questions.")
        return redirect(f'/questions/{len(session["responses"])}')

    question = survey.questions[int(question_id)]

    return render_template('question.html', question = question)

@app.post('/answer')
def handle_answers():
    """Appends answers to session[“responses”] list and redirects to new question
    if available. If not it redirects to the thank you page"""
    selected_choice = request.form['answer']
    selected_choices = session["responses"]
    selected_choices.append(selected_choice)
    session["choices"] = selected_choices
    if len(session["responses"]) >= len(survey.questions):
        return redirect('/thankyou')

    question_number = len(session["responses"])

    return redirect(f'/questions/{question_number}')

@app.get('/thankyou')
def get_thank_you_message():
    """Returns a thank you message with questions and answers"""
    survey_questions = survey.questions
    active_responses = session["responses"]
    return render_template(
        'completion.html',
        survey_questions= survey_questions,
        active_responses=active_responses
        )