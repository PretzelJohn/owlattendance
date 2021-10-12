import sys
from app import db
from app.models import Users

if __name__ == '__main__':
    if len(sys.argv) != 3: sys.exit(0)

    u = Users(username=sys.argv[1])
    u.set_password(sys.argv[2])
    db.session.add(u)
    db.session.commit()