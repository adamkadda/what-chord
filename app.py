from flask import Flask, request, render_template, jsonify
from markupsafe import escape
from what_chord import what_chord

app = Flask(__name__)

from flask import url_for

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        json = request.json
        notes = json['notes']

        chords = what_chord(notes)

        for chord in chords:
            print(chord)

    return render_template('index.html')