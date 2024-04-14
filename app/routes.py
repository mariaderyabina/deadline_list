from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import CreateTaskForm, DeleteTaskForm
import datetime
import sqlalchemy as sa
from app import db
from app.models import Task

@app.route('/')
def home():
    create_form = CreateTaskForm()
    delete_form = DeleteTaskForm()
    today = datetime.date.today()
    deadline_list = db.session.scalars(sa.select(Task).order_by(Task.date)).all()
    return render_template('deadline_list.html', title='Deadline List', create_form=create_form, delete_form=delete_form, deadline_list=deadline_list, today=today)

@app.route('/create', methods=['POST'])
def create():
    create_form = CreateTaskForm()
    delete_form = DeleteTaskForm()
    if create_form.validate_on_submit():
        # добавить задачу
        task = Task(task=create_form.task.data, date=create_form.date.data)
        db.session.add(task)
        db.session.commit()
    today = datetime.date.today()
    deadline_list = db.session.scalars(sa.select(Task).order_by(Task.date)).all()
    # иначе вывести ошибку
    return render_template('deadline_list.html', title='Deadline List', create_form=create_form, delete_form=delete_form, deadline_list=deadline_list, today=today)

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    create_form = CreateTaskForm()
    delete_form = DeleteTaskForm()
    if delete_form.validate_on_submit():
        # удаление - еще понадобится
        #to_delete = db.session.scalar(sa.select(Task).where(Task.id==id))
        #db.session.delete(to_delete)
        task = db.session.scalar(sa.select(Task).where(Task.id==id))
        task.is_done = True
        db.session.commit()
    today = datetime.date.today()
    deadline_list = db.session.scalars(sa.select(Task).order_by(Task.date)).all()
    return render_template('deadline_list.html', title='Deadline List', create_form=create_form, delete_form=delete_form, deadline_list=deadline_list, today=today)


