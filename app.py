from flask import Flask, render_template, request, redirect, session, send_file
import os
from question_ai import generate_question_bank
from pdf_generator import create_pdf
import fitz
import pytesseract
from PIL import Image
app = Flask(__name__)
app.secret_key = "exam_secret"

UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "1234":
            session['user'] = username
            return redirect('/dashboard')
        else:
            return "Invalid Login"

    return render_template('login.html')

# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':

        subject = request.form['subject']
        paper_code = request.form['paper_code']
        marks = request.form['marks']
        difficulty = request.form['difficulty']

        syllabus_text = request.form['syllabus']

        file = request.files.get('file')

        # Upload file read
        if file and file.filename != '':

            filepath = os.path.join(
                app.config['UPLOAD_FOLDER'],
                file.filename
            )

            file.save(filepath)

            ext = file.filename.lower()

            # TXT
            if ext.endswith('.txt'):

                with open(
                    filepath,
                    'r',
                    encoding='utf-8'
                ) as f:

                    syllabus_text = f.read()

            # PDF
            elif ext.endswith('.pdf'):

                syllabus_text = ""

                pdf_file = fitz.open(
                    filepath
                )

                for page in pdf_file:

                    syllabus_text += (
                        page.get_text()
                    )

                pdf_file.close()

            # Image OCR
            elif (
                ext.endswith('.jpg')
                or ext.endswith('.jpeg')
                or ext.endswith('.png')
            ):

                img = Image.open(
                    filepath
                )

                syllabus_text = (
                    pytesseract
                    .image_to_string(img)
                )

        # Generate Question Bank
        question_bank = generate_question_bank(
            syllabus_text,
            difficulty
        )

        return render_template(
            'dashboard.html',
            question_bank=question_bank
        )

    return render_template(
        'dashboard.html',
        question_bank=None
    )

# PDF Download
@app.route('/download')
def download():

    if 'paper' not in session:
        return redirect('/dashboard')

    filename = create_pdf(session['paper'])

    return send_file(
        filename,
        as_attachment=True
    )
 # Final Paper Route
@app.route('/final_paper', methods=['POST'])
def final_paper():

    selected_questions = request.form.getlist(
        'selected_questions'
    )

    time_allowed = request.form.get(
        'time_allowed'
    )

    instructions = request.form.get(
        'instructions'
    )

    paper = f"""
UNIVERSITY EXAMINATION

FINAL QUESTION PAPER

Time Allowed : {time_allowed}

Instructions:
{instructions}
"""

    grouped = {}

    for item in selected_questions:

        if "||" in item:

            unit, question = item.split(
                "||",
                1
            )

            if unit not in grouped:
                grouped[unit] = []

            grouped[unit].append(
                question
            )

    q_no = 1

    for unit, questions in grouped.items():

        paper += (
            f"\n\n{unit.center(40)}\n"
        )

        for q in questions:

            paper += (
                f"\nQ{q_no}. {q}\n"
            )

            q_no += 1

    session['paper'] = paper

    return render_template(
        'result.html',
        paper=paper
    )

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('paper', None)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)