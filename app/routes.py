from app import app
from app.errors import not_found_error
from app.events import create_event, delete_event, update_event, get_event, get_event_list
from app.forms import LoginForm, EventsForm, ReportsForm, StudentForm, ChangePasswordForm
from app.models import Users, Major, Student
from app.report import generate_report
from app.students import add_student, delete_student, update_student

from flask import render_template, flash, redirect, url_for, request, send_file, make_response
from flask_login import current_user, login_user, logout_user, login_required

from markupsafe import Markup
from os.path import exists
from werkzeug.urls import url_parse


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '' or next_page == '/logout':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('main/login.html', title='Sign In', form=form)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('events'))
    return redirect(url_for('login'))


@app.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    form = ReportsForm()
    form.event_name.choices = [(e.event_id, e.get_date() + ' - ' + e.event_name) for e in get_event_list()]
    form.filter_by_major.choices = [('', 'None')] + [(m[0], m[0]) for m in Major.query.with_entities(Major.major_name).distinct().order_by(Major.major_name.asc()).all()]
    form.filter_by_department.choices = [('', 'None')] + [(d[0], d[0]) for d in Major.query.with_entities(Major.department).distinct().order_by(Major.department.asc()).all()]

    if form.validate_on_submit():
        e = get_event(form.event_name.data).first()
        filter_by_eq = ''
        if form.filter_by.data == 'ClassRank':
            filter_by_eq = form.filter_by_rank.data
        elif form.filter_by.data == 'MajorName':
            filter_by_eq = form.filter_by_major.data
        elif form.filter_by.data == 'Department':
            filter_by_eq = form.filter_by_department.data

        generate_report(e.event_id, form.columns.data, form.filter_by.data, filter_by_eq, form.sort_by.data,
                        form.sort_order.data)

        flash(Markup('Report generated successfully! Click <a href="' + url_for('report') +
                     '" class="alert-link">here</a> to view.'))
        return redirect(url_for('reports'))

    exist = exists('app/reports/report.html')
    return render_template('reports/reports.html', title='Create Reports', form=form, exist=exist)


@app.route('/reports/report', methods=['GET', 'POST'])
@login_required
def report():
    if exists('app/reports/report.html'):
        with open('app/reports/report.html', 'r') as f:
            return render_template('reports/report.html', title='Report', table=Markup(f.read()))
    return not_found_error()


@app.route('/reports/report/<extension>')
@login_required
def report_export(extension):
    if extension == 'xlsx':
        return send_file('reports/report.xlsx', as_attachment='report.xlsx')
    if extension == 'pdf':
        with open('app/reports/report.pdf', 'rb') as f:
            response = make_response(f.read())
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'inline; filename=report.pdf'
            return response
    if extension == 'html':
        with open('app/reports/report.html', 'r') as f:
            return render_template('reports/result.html', title='Report', table=Markup(f.read()))
    return redirect(url_for('report'))


@app.route('/events', methods=['GET', 'POST'])
@login_required
def events():
    form = EventsForm()
    if request.method == 'POST':
        key = ''
        for k in request.form.keys():
            key = k if '_' in k else ''
        if 'delete_' in key:
            return delete_event(int(key.split('_')[1]))
        if 'save_' in key:
            return update_event(int(key.split('_')[1]), request.form['event_name'], request.form['event_date'])
        if form.validate_on_submit():
            return create_event(form.event_name.data, form.event_date.data)

    event_list = get_event_list()
    return render_template('admin/events.html', title='Manage Events', form=form,
                           event_list=event_list, count=len(event_list))


@app.route('/events/<int:event_id>', methods=['GET', 'POST'])
@login_required
def attendance(event_id):
    e = get_event(event_id).first()
    if not e:
        return not_found_error()

    form = StudentForm()
    form.major.choices = [('', 'None')]
    form.major.choices += [(m.major_id, m.major_name) for m in Major.query.order_by(Major.major_name).all()]

    if request.method == 'POST':
        key = ''
        for k in request.form.keys():
            key = k if '_' in k else ''
        if 'delete_' in key:
            return delete_student(event_id, key.split('_')[1])
        if 'save_' in key:
            return update_student(event_id, key.split('_')[1], form.last_name.data, form.first_name.data,
                                  form.email.data, form.class_rank.data, form.major.data)
        if form.validate_on_submit():
            return add_student(event_id, form.ksu_id.data, form.last_name.data, form.first_name.data,
                               form.email.data, form.class_rank.data, form.major.data)

    student_list = e.attendance.order_by(Student.last_name).all()
    return render_template('admin/attendance.html', title='Attendance', form=form, name=e.event_name, date=e.get_date(),
                           student_list=student_list, majors=form.major.choices, count=len(student_list))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = ChangePasswordForm()
    if request.method == 'POST':
        user = Users.query.filter_by(username=current_user.username).first()
        if not user:
            flash('Please log in to access this page.')
            return redirect(url_for('login'))

        if form.validate_on_submit():
            if form.new.data != form.confirm.data:
                flash('"New password" must match "Confirm new password"!')
            elif user.check_password(form.current.data):
                user.set_password(form.confirm.data)
                flash('Your password was updated successfully!')
            else:
                flash('Invalid password for "Current password".')
            return redirect(url_for('account'))

    return render_template('admin/account.html', title='Change Password', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/favicon.ico')
def favicon():
    return ''
