from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80))
    deposit = db.Column(db.Float, default=0)

    good_user = db.relationship('GoodUser', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.name

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class GoodUser(db.Model):
    __tablename__ = 'GoodUser'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    symbol = db.Column(db.String(80))
    funding_rate = db.Column(db.Float)
    mark_price = db.Column(db.Float)
    index_price = db.Column(db.Float)
    interest_rate = db.Column(db.Float)
    direction = db.Column(db.Integer)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


