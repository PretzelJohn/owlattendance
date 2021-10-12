from app import db
from app.events import get_event
from app.models import Student, attendance
from flask import flash, redirect, url_for


def add_student(event_id, ksu_id, last_name, first_name, email, rank, major_id):
    event = get_event(event_id).first()

    ksu_id = '{:0>9}'.format(ksu_id)
    email = email if email else None
    rank = rank if rank else None
    major_id = major_id if major_id else None

    student = get_student(ksu_id).first()
    if student:
        student.last_name = last_name
        student.first_name = first_name
        if email:
            student.email_address = email
        if rank:
            student.class_rank = rank
        if major_id:
            student.major_id = major_id
    else:
        student = Student(ksu_id=ksu_id, last_name=last_name, first_name=first_name,
                          email_address=email, class_rank=rank, major_id=major_id)
        db.session.add(student)

    event.attendance.append(student)
    db.session.commit()
    flash_message(student, 'added')
    return get_redirect(event_id)


def delete_student(event_id, ksu_id):
    student = get_student(ksu_id)
    q = attendance.delete().where(attendance.c.KSUID == ksu_id)
    db.session.execute(q)

    flash_message(student.first(), 'deleted')
    student.delete()
    db.session.commit()
    return get_redirect(event_id)


def update_student(event_id, ksu_id, last_name, first_name, email, rank, major_id):
    if not last_name or not first_name:
        flash('Last Name and First name cannot be empty!')
        return get_redirect(event_id)
    if not email:
        email = None
    if not rank:
        rank = None
    if not major_id:
        major_id = None

    student = get_student(ksu_id).first()
    flash_message(student, 'updated')
    student.last_name = last_name
    student.first_name = first_name
    student.email_address = email
    student.class_rank = rank
    student.major_id = major_id

    db.session.commit()
    return get_redirect(event_id)


def flash_message(student, operation):
    flash('Student "' + student.first_name + ' ' + student.last_name + '" ' + operation + ' successfully!')


def get_student(ksu_id):
    return Student.query.filter_by(ksu_id=ksu_id)


def get_redirect(event_id):
    return redirect(url_for('attendance', event_id=event_id))
