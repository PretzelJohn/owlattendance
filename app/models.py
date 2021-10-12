from app import db, login
from datetime import date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


attendance = db.Table('attendance',
    db.Column('EventID', db.INT, db.ForeignKey('event.EventID'), primary_key=True),
    db.Column('KSUID', db.CHAR(9), db.ForeignKey('student.KSUID'), primary_key=True)
)


class Users(db.Model, UserMixin):
    user_id = db.Column(db.INT, name='UserID', primary_key=True)
    username = db.Column(db.CHAR(25), name='Username', index=True, unique=True)
    password_hash = db.Column(db.CHAR(100), name='PasswordHash')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(str(self.password_hash).rstrip(), password)

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Event(db.Model):
    event_id = db.Column(db.INT, name='EventID', primary_key=True)
    event_name = db.Column(db.VARCHAR(250), name='EventName', nullable=False)
    event_date = db.Column(db.DATE, name='EventDate', nullable=False, index=True, default=date.today())
    attendance = db.relationship('Student', secondary=attendance, lazy='dynamic', backref=db.backref('events', lazy=True))

    def get_year(self):
        return str(self.event_date.year)

    def get_date(self):
        return self.event_date.strftime('%m/%d/%Y')

    def set_date(self, event_date):
        values = event_date.split('-')
        self.event_date = date(int(values[0]), int(values[1]), int(values[2]))

    def __repr__(self):
        return '<Event {}, {}>'.format(self.event_name, self.event_date)


class Student(db.Model):
    ksu_id = db.Column(db.CHAR(9), name='KSUID', primary_key=True)
    last_name = db.Column(db.VARCHAR(50), name='LastName', nullable=False)
    first_name = db.Column(db.VARCHAR(50), name='FirstName', nullable=False)
    email_address = db.Column(db.VARCHAR(100), name='EmailAddress', nullable=True)
    class_rank = db.Column(db.CHAR(10), name='ClassRank', nullable=True)
    major_id = db.Column(db.INT, db.ForeignKey('major.MajorID'), name='MajorID', nullable=True)

    def get_rank(self):
        if not self.class_rank:
            return ''
        return self.class_rank.rstrip()

    def __repr__(self):
        return '<Student {}, {}, {}>'.format(self.last_name, self.first_name, self.class_rank)


class Major(db.Model):
    major_id = db.Column(db.INT, name='MajorID', primary_key=True)
    major_name = db.Column(db.CHAR(100), name='MajorName', nullable=False)
    department = db.Column(db.CHAR(75), name='Department', nullable=False)
    students = db.relationship('Student', backref='major', lazy=True)

    def __repr__(self):
        return '<Major {}, {}>'.format(self.major_name, self.department)
