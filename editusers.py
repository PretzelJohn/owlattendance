import sys
from app import db
from app.models import Users

if __name__ == '__main__':
    if len(sys.argv) < 1: sys.exit(0)
    if len(sys.argv) == 2 and sys.argv[1] == "list":
        users = db.session.query(Users).order_by(Users.user_id.asc()).all()
        print("List of current usernames:")
        for user in users:
            print("{:>5}: {}".format(user.user_id, user.username))
    elif len(sys.argv) == 3 and sys.argv[1] == "del":
        id = sys.argv[2]
        db.session.query(Users).filter(Users.user_id == id).delete()
        db.session.commit()
    elif len(sys.argv) == 4 and sys.argv[1] == "add":
        u = Users(username=sys.argv[2])
        u.set_password(sys.argv[3])
        db.session.add(u)
        db.session.commit()
    else:
        print("Usage:")
        print("  list")
        print("  add <username> <password>")
        print("  del <user_id>")
