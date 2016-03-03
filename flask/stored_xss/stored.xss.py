from flask import Flask, render_template, request, make_response, url_for, session, redirect
from flask.ext.pymongo import PyMongo
import random
import string

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://xssuser:xsspass@localhost:27017/xss?ssl=true'
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.secret_key = 'S3cr3t k3Y!!!*'
mongo = PyMongo(app)


@app.route('/')
def index():
    return mongo.db
    if 'username' in session:
        users = mongo.db.user.find()
        return render_template('dashboard.html', users=users)
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        user = mongo.db.user.find_one({'username': session.get('username')})
        return render_template('profile.html', user=user)
    else:
        u = session.get('username')
        d = request.form['display']
        c = request.form['cc_num']
        mongo.db.user.update({'username': u}, {'$set': {'display': d, 'cc_num': c}})
        return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        user = mongo.db.user.find_one({'username': u, 'password': p})
        print(user)
        if not user:
            return render_template('login.html')
        session['username'] = u
        return redirected(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
