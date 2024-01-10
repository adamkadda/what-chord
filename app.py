from flask import Flask, request, render_template
from markupsafe import escape

app = Flask(__name__)

from flask import url_for

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        # validate user input
        # run user input through chord identifier
            # helper functions also sort output
        # insert into db

        return render_template('results.html', )
    
    return render_template('index.html')
