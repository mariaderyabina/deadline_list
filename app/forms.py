from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class CreateTaskForm(FlaskForm):
    task = StringField('Новая задача', validators=[DataRequired()])
    date = DateField('Дедлайн', validators=[DataRequired()])
    submit = SubmitField('Добавить задачу')

class StatusDoneForm(FlaskForm):
    submit = SubmitField('Сделано')

class StatusNotDoneForm(FlaskForm):
    submit = SubmitField('Не сделано')
    
class DeleteTaskForm(FlaskForm):
    submit = SubmitField('Удалить')