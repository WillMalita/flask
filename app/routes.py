from flask import render_template, redirect, flash, request, url_for, jsonify
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'wmalita'}
    classes = [{'classInfo': {'code': 'CSC324', 'title': 'DevOps'}, 'instructor': 'Baoqiang Yan'},
               {'classInfo': {'code': 'CSC346', 'title': 'Enterprise Systems in Java'}, 'instructor': 'Evan Noynaert'},
               {'classInfo': {'code': 'SEC300', 'title': 'Intro to Cybersecurity'}, 'instructor': 'Yipkei Kwok'}]
    return render_template('index.html', title='Home', user=user, classes=classes)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            credentials = {"username": form.username.data, "password": form.password.data}
            response = requests.post(url_for('loginAPI', _external=True), json=credentials)
            dict = response.json()
            if dict['Success']:
                flash('Welcome user {}({})! You opted for remember_me={}'.format(form.username.data, dict['uid'],
                                                                               form.remember_me.data))
                return redirect(url_for('index'))
            else:
                flash('Invalid credentials')
    else:
        if request.args:
            flash('GET method now allowed for login!')
        # else:
        #   flash('No data in request!')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/json')
def jsonTest():
    # return jsonify(list(range(5)))
    instructor = {"username": "byan",
                  "role": "instructor",
                  "uid": 11,
                  "name":
                      {"firstname": "Baoqiang",
                       "lastname": "Yan"
                       }
                  }
    return jsonify(instructor)


@app.route('/restlogin', methods=['GET', 'POST'])
def loginAPI():
    json_data = request.get_json(force=True)
    if json_data:
        username = json_data["username"]
        password = json_data["password"]
    else:
        return '{"Success":false}'
    if username == 'byan' and password == '123':
        return '{"Success":true}'
    return '{"Success":false}'

