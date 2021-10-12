from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, SelectMultipleField, BooleanField, widgets
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional


class CheckboxGroup(SelectMultipleField):
    widget = widgets.ListWidget()
    option_widget = widgets.CheckboxInput()


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired('Please enter your username.')], render_kw={'class': 'form-control field-top', 'required': True, 'autocomplete': 'username', 'maxlength': '25'})
    password = PasswordField('Password:', validators=[DataRequired('Please enter your password.')], render_kw={'class': 'form-control field-bot', 'required': True, 'autocomplete': 'current-password'})
    remember = BooleanField('Remember me', default=False, id="rememberMe")
    submit = SubmitField('Sign in')


class ChangePasswordForm(FlaskForm):
    current = PasswordField('Current password:', validators=[DataRequired()], render_kw={'class': 'form-control field-top', 'required': True, 'autocomplete': 'current-password'})
    vs = [DataRequired(), Length(8, message='New passwords must be 8 or more characters.')]
    new = PasswordField('New password:', validators=vs, render_kw={'class': 'form-control field-mid', 'required': True, 'autocomplete': 'new-password', 'minlength': '8'})
    confirm = PasswordField('Confirm new password:', validators=vs, render_kw={'class': 'form-control field-bot', 'required': True, 'autocomplete': 'new-password', 'minlength': '8'})
    submit = SubmitField('Change password')


class EventsForm(FlaskForm):
    event_name = StringField('Event Name:', validators=[DataRequired('Please enter an event name.'), Length(-1, 250, 'The event name is too long.')], render_kw={'class': 'form-control field-top', 'required': True, 'autocomplete': 'off', 'maxlength': '250'})
    event_date = DateField('Event Date:', validators=[DataRequired('Please enter a valid event date.')], render_kw={'class': 'form-control field-bot', 'required': True, 'autocomplete': 'off', 'min': '1950-01-01', 'max': '2950-12-31'}, default=date.today)
    submit = SubmitField('Create event')

    def validate_event_date(form, field):
        if field.data < date(1950, 1, 1) or field.data > date(2950, 12, 31):
            raise ValidationError("The event date must be between 01/01/1950 and 12/31/2950.")


class StudentForm(FlaskForm):
    ksu_id = StringField('KSU ID:', validators=[DataRequired(), Length(9, 9, 'KSU ID must be exactly 9 digits')], render_kw={'class': 'form-control field', 'autocomplete': 'off', 'required': True, 'minlength': '9', 'maxlength': '9', 'pattern': '\\d{9}'})
    first_name = StringField('First name:', validators=[DataRequired(), Length(max=50, message='The first name is too long.')], render_kw={'class': 'form-control field-top', 'autocomplete': 'off', 'required': True, 'maxlength': '50', 'pattern': '[\\w\\-\']+'})
    last_name = StringField('Last name:', validators=[DataRequired(), Length(max=50, message='The last name is too long.')], render_kw={'class': 'form-control field-bot', 'autocomplete': 'off', 'required': True, 'maxlength': '50', 'pattern': '[\\w\\-\']+'})
    email = EmailField('Email (optional):', validators=[Optional(), Email('Please enter a valid email address.'), Length(max=100, message='The email is too long.')], render_kw={'class': 'form-control field', 'autocomplete': 'off', 'maxlength': '100'})
    class_rank = SelectField('Class rank (optional):', validators=[Optional(), Length(max=10, message='The class rank is too long.')], choices=[('', 'None'), ('Freshman', 'Freshman'), ('Sophomore', 'Sophomore'), ('Junior', 'Junior'), ('Senior', 'Senior'), ('Other', 'Other')], render_kw={'class': 'form-select field', 'autocomplete': 'off'})
    major = SelectField('Major (optional):', validators=[Optional()], choices=[], render_kw={'class': 'form-select field', 'autocomplete': 'off'})
    submit = SubmitField('Add student')

    def validate_ksu_id(form, field):
        try:
            int(field.data)
        except:
            raise ValidationError("KSU ID must be a 9-digit number.")


class ReportsForm(FlaskForm):
    event_name = SelectField('Event name:', validators=[DataRequired()], choices=[], render_kw={'class': 'form-select field', 'required': True})
    columns = CheckboxGroup('Student columns:', validators=[DataRequired()], choices=[('KSUID', 'KSU ID'), ('LastName', 'Last name'), ('FirstName', 'First name'), ('EmailAddress', 'Email'), ('ClassRank', 'Class rank'), ('MajorName', 'Major'), ('Department', 'Department')], default=['LastName', 'FirstName', 'ClassRank', 'MajorName', 'Department'])
    filter_by = SelectField('Filter by (optional):', validators=[Optional()], choices=[('', 'None'), ('ClassRank', 'Class rank'), ('MajorName', 'Major'), ('Department', 'Department')], render_kw={'class': 'form-select field'}, id='filterBy')
    filter_by_rank = SelectField('Where "Class Rank" =', validators=[Optional()], choices=[('', 'None'), ('Freshman', 'Freshman'), ('Sophomore', 'Sophomore'), ('Junior', 'Junior'), ('Senior', 'Senior'), ('Other', 'Other')], render_kw={'class': 'form-select field-bot'}, id='filterByRank')
    filter_by_major = SelectField('Where "Major" =', validators=[Optional()], choices=[], render_kw={'class': 'form-select field-bot'}, id='filterByMajor')
    filter_by_department = SelectField('Where "Department" =', validators=[Optional()], choices=[], render_kw={'class': 'form-select field-bot'}, id='filterByDepartment')
    sort_by = SelectField('Sort by:', validators=[DataRequired()], choices=[('LastName', 'Last name'), ('FirstName', 'First name'), ('ClassRank', 'Class rank'), ('MajorName', 'Major'), ('Department', 'Department')], render_kw={'class': 'form-select field', 'required': True})
    sort_order = SelectField('Sort order:', validators=[DataRequired()], choices=[('ASC', 'Ascending (A→Z)'), ('DESC', 'Descending (Z→A)')], render_kw={'class': 'form-select field', 'required': True})
    submit = SubmitField('Generate report')
