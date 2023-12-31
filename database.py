from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship

from ma import ma

db = SQLAlchemy()


# common fields
class TimestampMixin(object):
    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=datetime.now(), nullable=False)

    @declared_attr
    def updated_at(cls):
        return db.Column(
            db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False
        )

    @declared_attr
    def deleted_at(cls):
        return db.Column(db.DateTime)


class User(UserMixin, db.Model, TimestampMixin):
    """User table
    This is kind of master table.
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tasks = relationship("Task", backref="users", cascade="all")


class UserSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "email",
            "password",
            "created_at",
            "updated_at",
        )


class Task(db.Model, TimestampMixin):
    """Task table
    This is kind of transaction table.
    """

    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    description = db.Column(db.String(255), nullable=False)


class TaskSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "user_id",
            "description",
            "created_at",
            "updated_at",
        )
