from flask import Flask, render_template, request, redirect, url_for, session
import os  # Miscellaneous operating system interfaces
import inspect  # Inspect live objects

_SERVER_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

template_folder = f'{_SERVER_PATH}/www'
static_folder = f'{template_folder}/static'
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.secret_key = 'your_secret_key'  # Needed for session management

# Home route
@app.route('/')
def index():
    return render_template('index.html', max_score=session.get('max_score'))

# Quiz submission route
@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    correct_answers = {'q1': 'correct', 'q2': 'correct', 'q3': 'correct'}
    score = 0
    for question, correct_answer in correct_answers.items():
        if request.form.get(question) == correct_answer:
            score += 1

    session['score'] = score
    session['max_score'] = max(score, session.get('max_score', 0))

    return redirect(url_for('result'))

# Result route
@app.route('/result')
def result():
    return render_template('result.html', score=session.get('score'), max_score=session.get('max_score'))

if __name__ == '__main__':
    app.run(debug=True)
