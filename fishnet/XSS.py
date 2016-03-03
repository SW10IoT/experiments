from flask import Flask, render_template, request, make_response
import random
import string
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"  # return a string

@app.route('/example1', methods =['GET'])
def example1():
    param = request.args.get('param', 'not set')
    resp = make_response(render_template('example1.html', param = param))
    resp.set_cookie('session_id',''.join(random.choice(string.ascii_uppercase) for x in range(16)))
    return resp

@app.route('/example2')
def example2():
    return render_template('example2_form.html')

@app.route('/example2action',methods = ['POST'])
def example2_action():
    resp = make_response(render_template('example2_response.html',  data = request.form[',my_text']))
    resp.set_cookie('session_id', ''.join(random.choice(string.ascii_uppercase) for x in range(16)))
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 4000,debug= True)
