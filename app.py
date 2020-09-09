from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'sgp'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/sgp'

mongo = PyMongo(app)


@app.route('/')
def index():
    if 'username' in session:
        x=mongo.db.Data.find()
        return render_template('main.html',x=x)

    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if request.form['pass'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))



@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass =request.form['pass']
            users.insert({'name': request.form['username'], 'password': hashpass, 'Phone_No':request.form['p_no'], 'Age': request.form['age']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username',None)
        return render_template('index.html')
    else:
        return '<p>User already logged out</p>'


@app.route('/recommend')
def recommend():
    x = mongo.db.Recommend.find()
    return render_template('recommend.html',x=x)


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)