from flask import Flask, request, render_template, jsonify, redirect, url_for, session
import sqlite3
import random


app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session management

class User():
    user=()
    def __init__(self):
        self.conn = sqlite3.connect('manager.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS USER (NAME TEXT, CONTACT TEXT, EMAIL TEXT, PASS TEXT, SCORE INT)")
        self.conn.commit()
    
    def register(self, data):
        try:
            self.cursor.execute("INSERT INTO USER (NAME, CONTACT, EMAIL, PASS, SCORE) VALUES (?,?,?,?,?)", 
                                (data[0], data[1], data[2], data[3], 0))
            self.conn.commit()
            return True
        except Exception as e:
            print("Something went wrong:", e)
            return False
    
    def login(self, email, password):
        self.cursor.execute("SELECT * FROM USER WHERE EMAIL = ?", (email,))
        user = self.cursor.fetchone()
        print("User:", user)
        if user[3] == password:
            session['user'] = user
            # print("Password:", password)
            return True
        return False
    
    def update_score(self, email, score):
        try:
            self.cursor.execute("UPDATE USER SET SCORE = ? WHERE EMAIL = ?", (score, email))
            self.conn.commit()
            print("Updated", score)
            return True
        except Exception as e:
            print("Failed to update score:", e)
            return False

class Quiz():
    def __init__(self):
        self.conn = sqlite3.connect('manager.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS QUESTIONBANK (QUESTION TEXT, OP1 TEXT, OP2 TEXT, OP3 TEXT, OP4 TEXT, ANS TEXT)")
        self.conn.commit()

    def fetch_questions_list(self):
        self.cursor.execute("SELECT * FROM QUESTIONBANK ORDER BY RANDOM() LIMIT 10")
        que_list = self.cursor.fetchall()
        questions = []
        for q in que_list:
            questions.append({
                'que': q[0],
                'ops': [q[1], q[2], q[3], q[4]],
                'ans': q[5]
            })
        return questions

user_model = User()
quiz_model = Quiz()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register_profile', methods=['POST'])
def register_profile():
    data = request.json
    if user_model.register(data):
        return jsonify({'message': 'Register successful', 'redirect_url': url_for('home')})
    else:
        return jsonify({'message': 'Register failed'})

@app.route('/login_profile', methods=['POST'])
def login_profile():
    data = request.json
    print("Login profile",data)
    if user_model.login(data[0], data[1]):
        # print("Login successful",session)
        return jsonify({'message': 'Login successful', 'redirect_url': url_for('home')})
    else:
        return jsonify({'message': 'Login failed'})

@app.route('/home')
def home():
    if 'user' in session:
        questions = quiz_model.fetch_questions_list()
        session['questions'] = questions
        return render_template('home.html', li=questions, profiles=session['user'])
    else:
        return redirect(url_for('index'))

@app.route('/attempt_quiz')
def attempt_quiz():
    session['score'] = 0
    return redirect(url_for('home'))

@app.route('/submit_option', methods=['POST'])
def submit_option():
    if 'questions' in session:
        data = request.json
        selected_option = data.get('option')
        correct_answers = [q['ans'] for q in session['questions']]
        if selected_option in correct_answers:
            
            session['score'] = session.get('score', 0) + 10
            correct_answers.remove(selected_option)
            print(f"Score: {session['score']}")
            user_model.update_score(session['user'][2], session['score'])
        return jsonify({'message': f"Selected option: {selected_option}", 'score': session['score']})
    return jsonify({'message': 'No active quiz session'})

@app.route('/view_profile')
def view_profile():
    if 'user' in session:
        return render_template('home.html', li=session.get('questions', []), profiles=session['user'])
    return redirect(url_for('index'))

@app.route('/update_profile', methods=['POST'])
def update_profile():
    data = request.json
    email = session['user'][2]
    try:
        for key, value in data.items():
            user_model.cursor.execute(f"UPDATE USER SET {key.upper()} = ? WHERE EMAIL = ?", (value, email))
        user_model.conn.commit()
        return jsonify({'message': 'Profile updated successfully'})
    except Exception as e:
        return jsonify({'message': 'Failed to update profile', 'error': str(e)})

@app.route('/scores')
def scores():
    if 'user' in session:
        return render_template('home.html', li=session.get('questions', []), profiles=session['user'])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
        