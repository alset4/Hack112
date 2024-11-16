from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)

app.secret_key = 'penis'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game1', methods=['GET', 'POST'])
def game1():
    # Handle the POST request
    if request.method == 'POST':
        # Collect the names from the form for 10 players (5 for each team)
        team1 = [
            request.form['name1'],
            request.form['name2'],
            request.form['name3'],
            request.form['name4'],
            request.form['name5']
        ]
        team2 = [
            request.form['name6'],
            request.form['name7'],
            request.form['name8'],
            request.form['name9'],
            request.form['name10']
        ]
        
        # Store the teams in the session (optional, for persistence)
        session['team1'] = team1
        session['team2'] = team2
        
        # Directly render the results page with the submitted data
        return render_template('results.html', team1=team1, team2=team2)

    # For GET request, just render the form without the teams populated yet
    return render_template('game1.html')

@app.route('/results')
def results():
    # Retrieve the teams from the session or query parameters
    team1 = session.get('team1', [])
    team2 = session.get('team2', [])
    
    return render_template('results.html', team1=team1, team2=team2)

if __name__ == '__main__':
    app.run(debug=True)
