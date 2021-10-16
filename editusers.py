import sys
from app import db
from app.models import Users

if __name__ == '__main__':
    if len(sys.argv) < 1: sys.exit(0)
    if len(sys.argv) == 1:
        print("Usage:")
        print("  list")
        print("  add <username> <password>")
        print("  del <username>")
    elif len(sys.argv) == 2 and sys.argv[1] == "list":
        
    if(sys.argv[1] == "")

    u = Users(username=sys.argv[1])
    u.set_password(sys.argv[2])
    db.session.add(u)
    db.session.commit()
