from datetime import datetime
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
    
class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)    
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    tasks: so.WriteOnlyMapped['Task'] = so.relationship(back_populates='user')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    task: so.Mapped[str] = so.mapped_column(sa.String(256), index=True)
    date: so.Mapped[datetime.date] = so.mapped_column(sa.DateTime, index=True)
    is_done: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    user: so.Mapped['User'] = so.relationship(back_populates='tasks')

    def __repr__(self):
        return '<id {}>'.format(self.id) + '<task {}>'.format(self.task) + '<date {}>'.format(self.date) + '<is_done {}>'.format(self.is_done)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))