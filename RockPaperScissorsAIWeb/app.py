from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key

# Moves and beats mapping
MOVES = ['rock', 'paper', 'scissors']
BEATS = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}

def get_ai_move(player_history):
    total_moves = sum(player_history.values())
    if total_moves < 3:
        return random.choice(MOVES)
    if random.random() < 0.8:
        most_common = max(player_history, key=player_history.get)
        return BEATS[most_common]
    else:
        return random.choice(MOVES)

def get_result(player_move, computer_move):
    if player_move == computer_move:
        return 'Tie'
    elif (player_move == 'rock' and computer_move == 'scissors') or \
         (player_move == 'paper' and computer_move == 'rock') or \
         (player_move == 'scissors' and computer_move == 'paper'):
        return 'Win'
    else:
        return 'Lose'

@app.route("/", methods=['GET', 'POST'])
def index():
    computer_move = None
    result = None

    # Initialize session variables
    if 'score' not in session:
        session['score'] = {'Win': 0, 'Lose': 0, 'Tie': 0}
    if 'player_history' not in session:
        session['player_history'] = {'rock': 0, 'paper': 0, 'scissors': 0}

    if request.method == 'POST':
        player_move = request.form['move']
        session['player_history'][player_move] += 1

        computer_move = get_ai_move(session['player_history'])
        result = get_result(player_move, computer_move)

        session['score'][result] += 1

    return render_template('index.html', computer_move=computer_move, result=result,
                           score=session['score'], player_history=session['player_history'])

@app.route("/reset")
def reset():
    session.pop('score', None)
    session.pop('player_history', None)
    return render_template('index.html', computer_move=None, result=None,
                           score={'Win': 0, 'Lose': 0, 'Tie': 0}, player_history={'rock': 0, 'paper': 0, 'scissors': 0})

if __name__ == "__main__":
    app.run(debug=True)
