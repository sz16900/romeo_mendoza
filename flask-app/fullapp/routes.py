from flask import render_template, flash, redirect, url_for, request
from fullapp import app, db
from fullapp.forms import LoginForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from fullapp.models import User, Post

@app.route('/')

# this can become the admin's dashboard
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", title='Home Page', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/post', methods=['GET', 'POST'])
# @login_required
def post():
    if current_user.is_authenticated:
        # return redirect(url_for('post'))
        form = PostForm()
        if form.validate_on_submit():
            post = Post(title=form.title.data, body=form.body.data)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('post.html', title='Post', form=form)
    else:
        return redirect(url_for('login'))
