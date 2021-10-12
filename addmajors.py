from app import db
from app.models import Major

if __name__ == '__main__':
    with open('majors.csv', 'r') as f:
        line = f.readline()
        line = f.readline()
        while line:
            tokens = line.split(',')
            major = Major(major_id=int(tokens[0]), major_name=tokens[1], department=tokens[2].rstrip())
            db.session.merge(major)
            db.session.commit()
            line = f.readline()
