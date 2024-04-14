import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
import datetime

class Task(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    task: so.Mapped[str] = so.mapped_column(sa.String(256), index=True)
    date: so.Mapped[datetime.date] = so.mapped_column(sa.DateTime, index=True)
    is_done: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)

    def __repr__(self):
        return '<id {}>'.format(self.id) + '<task {}>'.format(self.task) + '<date {}>'.format(self.date) + '<is_done {}>'.format(self.is_done)