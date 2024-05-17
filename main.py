from flask import Flask, request, render_template,jsonify, redirect, url_for
from user import User
from quiz import Quiz
import sqlite3
import random


User = User()
Quiz = Quiz()

app = Flask(__name__)

que_list =[]
ans = []
score = 0  # Initialize score as a global variable

for q in que_list:
    ans.append(q['ans'])
    
print(ans)




@app.route('/')
def index():
    return render_template('index.html')



@app.route('/register_profile', methods=['POST'])
def register_profile():
    data = request.json
    # Process the data as required
    print(data)
    if User.register(data):
        print("Registered")
        return jsonify({'message': 'register successful', 'redirect_url': url_for('home')})
    else:
        return jsonify({'message': 'register failed'})


@app.route('/login_profile', methods=['POST'])
def login_profile():
    data = request.json
    print("data",data)
    if User.login(data[0], data[1]):
        print("Logged in",User.user)
        return jsonify({'message': 'register successful', 'redirect_url': url_for('home')})
    else:
        return jsonify({'message': 'profile login successfully'})



@app.route('/home')
def home():
    global que_list
    que_list = Quiz.fetch_questions_list()
    return render_template('home.html', li=que_list, profiles=User.user)


@app.route('/attempt_quiz')
def attemt_quiz():
    global score 
    score = 0  
    return render_template('home.html', li=que_list)


@app.route('/submit_option', methods=['POST'])
def submit_option():
    global score  
    data = request.json
    selected_option = data.get('option')
    
    if selected_option in ans:
        score += 10
        ans.remove(selected_option)
        print(f"Score: {score}")
        cursor.execute(f"UPDATE USER SET SCORE={score} WHERE EMAIL= {User.user[2]}")
        conn.commit()
    
    return jsonify({'message': f"Selected option: {selected_option}"})


@app.route('/view_profile')
def view_profile():
    return render_template('home.html',li=que_list,profiles=User.user)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    data = request.json
    print(data)
    
    if i in data and i not in User.user:
        profiles[i] = data[i]
        print(profiles)
        cursor.execute(f"UPDATE USER SET {i} = {data[i]} WHERE EMAIL= {User.user[2]}")
        conn.commit()
    
    return jsonify({'message': 'Profile updated successfully'})





@app.route('/scores')
def scores():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
