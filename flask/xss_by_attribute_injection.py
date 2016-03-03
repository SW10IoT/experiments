from flask import Flask
from flask import render_template

app = Flask(__name__)

html = open('templates/index.html').read()

@app.route('/<href>')
def index(href):
    return html

if __name__ == '__main__':
    app.run(debug=True)


# Browsers fix this
