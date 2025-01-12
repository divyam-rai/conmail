from app.db import db

class Base(db.Model):
    __abstract__ = True