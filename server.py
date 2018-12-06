from flask import Flask, render_template, request, jsonify
import datetime
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open('status.json') as status_file:
        status = json.load(status_file)
        occupied = status['occupied']
        meeting = status['meeting']
        last_updated = status['last_updated']
        return render_template('index.html',occupied=occupied,meeting=meeting,last_updated=last_updated)

if __name__ == '__main__':
    app.run(debug=False)
