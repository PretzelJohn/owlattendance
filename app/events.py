from flask import flash, redirect, url_for

from app import db
from app.models import Event, attendance


def create_event(name, date):
    event = Event(event_name=name[:250], event_date=date)
    db.session.add(event)
    db.session.commit()
    flash_message(event, 'created')
    return get_redirect()


def delete_event(id):
    event = get_event(id)
    q = attendance.delete().where(attendance.c.EventID == id)
    db.session.execute(q)

    flash_message(event.first(), 'deleted')
    event.delete()
    db.session.commit()
    return get_redirect()


def update_event(id, name, date):
    if not name or not date:
        flash('Event Name and Event Date cannot be empty!')
        return get_redirect()
    event = get_event(id).first()
    flash_message(event, 'updated')
    event.event_name = name[:250]
    event.set_date(date)
    db.session.commit()
    return get_redirect()


def flash_message(event, operation):
    flash('Event "' + event.event_name + '" on ' + event.get_date() + ' ' + operation + ' successfully!')


def get_event(id):
    return Event.query.filter_by(event_id=id)


def get_event_list(asc=True):
    order = Event.event_date.asc if asc else Event.event_date.desc
    return Event.query.order_by(order()).all()


def get_redirect():
    return redirect(url_for('events'))
