from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class CreateTaskForm(FlaskForm):
    task = StringField('Новая задача', validators=[DataRequired()])
    date = DateField('Дедлайн', validators=[DataRequired()])
    submit = SubmitField('Добавить задачу')

class DeleteTaskForm(FlaskForm):
    submit = SubmitField('Сделано')