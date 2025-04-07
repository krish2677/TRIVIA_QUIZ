from flask import Flask, render_template, request, redirect, session, url_for
import requests
import random
import json
import os
import html

# Category ID to Name Mapping
CATEGORY_MAP = {
    "9": "General Knowledge",
    "10": "Entertainment: Books",
    "11": "Entertainment: Film",
    "12": "Entertainment: Music",
    "13": "Entertainment: Musicals & Theatres",
    "14": "Entertainment: Television",
    "15": "Entertainment: Video Games",
    "16": "Entertainment: Board Games",
    "17": "Science & Nature",
    "18": "Science: Computers",
    "19": "Science: Mathematics",
    "20": "Mythology",
    "21": "Sports",
    "22": "Geography",
    "23": "History",
    "24": "Politics",
    "25": "Art",
    "26": "Celebrities",
    "27": "Animals",
    "28": "Vehicles",
    "29": "Comics",
    "30": "Gadgets",
    "31": "Anime & Manga",
    "32": "Cartoon & Animations"
}

app = Flask(__name__)
app.secret_key = 'secret-key'

API_URL = "https://opentdb.com/api.php?amount=1&type=multiple"
LEVELS = [1000, 2000, 3000, 5000, 10000, 20000, 40000, 80000, 160000, 320000, 640000, 1250000, 2500000, 5000000, 10000000, 70000000]
LEADERBOARD_FILE = 'leaderboard.json'

def get_question():
    category = session.get('category')
    url = API_URL
    if category:
        url += f"&category={category}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["results"][0]
        question = html.unescape(data["question"])
        correct = html.unescape(data["correct_answer"])
        options = [html.unescape(opt) for opt in data["incorrect_answers"] + [correct]]
        random.shuffle(options)
        return question, options, correct
    return None, [], None

def save_leaderboard(name, money, category_id, level):
    category_name = CATEGORY_MAP.get(str(category_id), f"Category {category_id}")
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'r') as file:
            leaderboard = json.load(file)
    else:
        leaderboard = []

    leaderboard.append({
        "name": name,
        "money": money,
        "category": category_name,
        "level": level
    })

    # Sort by level first, then by money
    leaderboard = sorted(leaderboard, key=lambda x: (x["level"], x["money"]), reverse=True)[:10]

    with open(LEADERBOARD_FILE, 'w') as file:
        json.dump(leaderboard, file)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['money'] = 0
        session['level'] = 0
        session['used_5050'] = False
        session['used_skip'] = False
        session['category'] = request.form['category']
        return redirect(url_for('question'))
    return render_template('index.html', categories=CATEGORY_MAP)

@app.route('/question', methods=['GET', 'POST'])
def question():
    level = session.get('level', 0)
    timer_limit = get_timer_for_level(level)

    if request.method == 'POST':
        if 'lifeline' in request.form:
            lifeline = request.form['lifeline']
            question = session['current_question']
            correct = session['correct']
            options = session['current_options']

            if lifeline == '5050' and not session.get('used_5050'):
                session['used_5050'] = True
                reduced = [correct]
                incorrects = [opt for opt in options if opt != correct]
                reduced.append(random.choice(incorrects))
                while len(reduced) < 4:
                    reduced.append(None)
                random.shuffle(reduced)
                session['current_options'] = reduced
                return render_template('question.html',
                                       question=question,
                                       options=session['current_options'],
                                       correct=correct,
                                       level=level,
                                       amount=LEVELS[level],
                                       timer=timer_limit)

            elif lifeline == 'skip' and not session.get('used_skip'):
                session['used_skip'] = True
                question, options, correct = get_question()
                session['current_question'] = question
                session['current_options'] = options
                session['correct'] = correct
                return render_template('question.html',
                                       question=question,
                                       options=options,
                                       correct=correct,
                                       level=level,
                                       amount=LEVELS[level],
                                       timer=timer_limit)

        elif 'option' in request.form:
            selected = request.form['option']
            correct = session.get('correct')

            if selected == correct:
                session['level'] += 1
                if session['level'] in [4, 9, 15]:
                    session['money'] = LEVELS[session['level']]
                if session['level'] >= len(LEVELS):
                    save_leaderboard(session['name'], LEVELS[-1], session.get('category', ''), session.get('level', 0))
                    redirect_url = url_for('won')
                else:
                    redirect_url = url_for('question')
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return {'correct': True, 'redirect_url': redirect_url}
                return redirect(redirect_url)

            else:
                save_leaderboard(session['name'], session.get('money', 0), session.get('category', ''), session.get('level', 0))
                redirect_url = url_for('lost')
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return {'correct': False, 'redirect_url': redirect_url}
                return redirect(redirect_url)

    question, options, correct = get_question()
    session['current_question'] = question
    session['current_options'] = options
    session['correct'] = correct

    return render_template('question.html',
                           question=question,
                           options=options,
                           correct=correct,
                           level=level,
                           amount=LEVELS[level],
                           timer=timer_limit)

def get_timer_for_level(level):
    if level <= 1:
        return 30
    elif level <= 6:
        return 45
    else:
        return 0

@app.route('/lost')
def lost():
    return render_template('lost.html', name=session.get('name'), money=session.get('money', 0))

@app.route('/won')
def won():
    return render_template('won.html', name=session.get('name'), money=LEVELS[-1])

@app.route('/leaderboard')
def leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        leaderboard_data = []
    else:
        with open(LEADERBOARD_FILE, 'r') as file:
            leaderboard_data = json.load(file)

    leaderboard_data.sort(key=lambda x: (x["level"], x["money"]), reverse=True)

    for i, entry in enumerate(leaderboard_data, 1):
        entry['rank'] = i

    return render_template("leaderboard.html", leaderboard=leaderboard_data)

if __name__ == "__main__":
    app.run(debug=True)
