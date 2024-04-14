from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import CreateTaskForm, StatusDoneForm, StatusNotDoneForm, DeleteTaskForm
import datetime
import sqlalchemy as sa
from app import db
from app.models import Task

@app.route('/')
def home():
    create_form = CreateTaskForm()
    status_done_form = StatusDoneForm()
    status_not_done_form = StatusNotDoneForm()
    delete_form = DeleteTaskForm()
    today = datetime.date.today()
    deadline_list = db.session.scalars(sa.select(Task).order_by(Task.date)).all()
    return render_template('deadline_list.html', title='Deadline List', create_form=create_form, status_done_form=status_done_form, status_not_done_form=status_not_done_form, delete_form=delete_form, deadline_list=deadline_list, today=today)

@app.route('/create', methods=['POST'])
def create():
    create_form = CreateTaskForm()
    if create_form.validate_on_submit():
        # добавить задачу
        task = Task(task=create_form.task.data, date=create_form.date.data)
        db.session.add(task)
        db.session.commit()
    today = datetime.date.today()
    deadline_list = db.session.scalars(sa.select(Task).order_by(Task.date)).all()
    return redirect(url_for('home'))

@app.route('/done/<id>', methods=['POST'])
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
def delete(id):
    delete_form = DeleteTaskForm()
    if delete_form.validate_on_submit():
        task = db.session.scalar(sa.select(Task).where(Task.id==id))
        db.session.delete(task)
        db.session.commit()
    today = datetime.date.today()
    deadline_list = db.session.scalars(sa.select(Task).order_by(Task.date)).all()
    return redirect(url_for('home'))
