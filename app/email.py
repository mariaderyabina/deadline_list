from flask_mail import Message
from app import app, mail
from flask import render_template

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_deadline_list(user, deadline_list):
    send_email(
        'Ваш список дедлайнов',
        sender=app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template('email/send_deadline_list.txt',
                                    user=user, deadline_list=deadline_list),
        html_body=render_template('email/send_deadline_list.html',
                                    user=user, deadline_list=deadline_list))        