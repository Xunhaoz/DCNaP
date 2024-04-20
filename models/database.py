from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80))

    def __repr__(self):
        return '<User %r>' % self.name

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Exchange(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
