from flask import Flask, request, render_template, jsonify
from what_chord import what_chord, clean_notes, note_to_int
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        json = request.json
        notes = json['notes']

        print(f'notes: {notes}')

        # generate tablename
        temp = clean_notes(notes) # clean then sort
        temp = sorted(note_to_int(temp)) # transform to integer notation
        key = 'chord_' + '_'.join(map(str, temp)) # typecast then join
        
        con = sqlite3.connect('chord_names.db')
        cur = con.cursor()

        # check if table exists in db (check 'key')
        # do (key,) to explicitly say that key is a single argument, since there are '_' chars 
        res = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (key,))

        if (res.fetchone() is None):
            print(f'table {key} DOES NOT EXIST')

            cur.execute(f"""
                CREATE TABLE {key} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    root TEXT NOT NULL,
                    conciseness INT NOT NULL,
                    inversion TEXT NOT NULL
                )
            """)

            print(f'table {key} created successfully')

            # obtain chords
            chords = what_chord(notes)

            # insert data into the table
            for chord in chords:
                
                # {'name': 'C', 'root': 'C', 'conciseness': 1, 'inversion': ('C', 'E', 'G')}

                inversion_str = ' '.join(chord['inversion'])
                chord['inversion_str'] = inversion_str

                query = f"""
                    INSERT INTO {key} (name, root, conciseness, inversion)
                    VALUES (:name, :root, :conciseness, :inversion_str)
                """

                cur.execute(query, chord)
                    
            con.commit()
            print(f'table {key} updated')

        query = f"""
            SELECT name, conciseness 
            FROM {key}
            ORDER BY conciseness, root
        """

        res = cur.execute(query)

        names = res.fetchall()

        for row in names:
            print(row)

        con.close()
        
        return render_template('results.html', res=names)
        # return '<h1>returned</h1>'

    return render_template('index.html')