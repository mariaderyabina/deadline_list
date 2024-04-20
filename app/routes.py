from app import app, db, mail
from flask import render_template, flash, redirect, url_for, request
from app.forms import CreateTaskForm, StatusDoneForm, StatusNotDoneForm, DeleteTaskForm, LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
import datetime
import sqlalchemy as sa
from app.models import Task, User
from urllib.parse import urlsplit
from app.email import send_deadline_list

@app.route('/')
@login_required
def home():
    create_form = CreateTaskForm()
    status_done_form = StatusDoneForm()
    status_not_done_form = StatusNotDoneForm()
    delete_form = DeleteTaskForm()
    today = datetime.date.today()
    deadline_list = db.session.scalars(sa.select(Task).where(Task.user_id==current_user.id).order_by(Task.date)).all()
    return render_template('deadline_list.html', title='Deadline List', create_form=create_form, status_done_form=status_done_form, status_not_done_form=status_not_done_form, delete_form=delete_form, deadline_list=deadline_list, today=today)

@app.route('/create', methods=['POST'])
@login_required
def create():
    create_form = CreateTaskForm()
    if create_form.validate_on_submit():
        task = Task(task=create_form.task.data, date=create_form.date.data, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
    today = datetime.date.today()
    deadline_list = db.session.scalars(sa.select(Task).order_by(Task.date)).all()
    return redirect(url_for('home'))

@app.route('/done/<id>', methods=['POST'])
@login_required
def done(id):
    status_done_form = StatusDoneForm()
    if status_done_form.validate_on_submit():
        task = db.session.scalar(sa.select(Task).where(Task.id==id))
        task.is_done = True
        db.session.commit()
    today = datetime.date.today()
    deadline_list = db.session.scalars(sa.select(Task).order_by(Task.date)).all()
    return redirect(url_for('home'))

@app.route('/not_done/<id>', methods=['POST'])
@login_required
def not_done(id):
    status_not_done_form = StatusNotDoneForm() 
    if status_not_done_form.validate_on_submit():
        task = db.session.scalar(sa.select(Task).where(Task.id==id))
        task.is_done = False
        db.session.commit()
    today = datetime.date.today()
    deadline_list = db.session.scalars(sa.select(Task).order_by(Task.date)).all()
    return redirect(url_for('home'))

@app.route('/delete/<id>', methods=['POST'])
@login_required
def delete(id):
    delete_form = DeleteTaskForm()
    if delete_form.validate_on_submit():
        task = db.session.scalar(sa.select(Task).where(Task.id==id))
        db.session.delete(task)
        db.session.commit()
    today = datetime.date.today()
    deadline_list = db.session.scalars(sa.select(Task).order_by(Task.date)).all()
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Неправильное имя пользователя или пароль')
            return redirect(url_for('login'))        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Вход', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляю, вы зарегистрированы!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)

@login_required
@app.route('/send_email', methods=['GET', 'POST'])
def send_email():
    deadline_list = db.session.scalars(sa.select(Task).where(Task.user_id==current_user.id).order_by(Task.date)).all()
    send_deadline_list(current_user, deadline_list)
    return redirect(url_for('home'))
