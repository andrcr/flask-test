from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired
import re



def validate_isbn(form, field):
    regex_string = r"^[A-Z]{4}-[0-9]{4}$"
    if not re.search(regex_string, field.data):
        raise ValidationError('Invalid fake ISBN')

def validate_update_field_name(form, field):
    acceptable_list = ["name", "author", "description"]
    if field.data not in acceptable_list:
        raise ValidationError('Invalid field name')
        
class AddingBooksForm(FlaskForm):
    name = StringField('Book name', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired(),validate_isbn])
    submit = SubmitField('Submit')

class UpdatingBooksForm(FlaskForm):
    isbn = StringField('ISBN', validators=[DataRequired(),validate_isbn])
    field_name = StringField('Field to be changed (name, author, description)', \
                             validators=[DataRequired(),validate_update_field_name])
    new_value = StringField('New value', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DeleteBooksForm(FlaskForm):
    isbn = StringField('ISBN', validators=[DataRequired(),validate_isbn])
    submit = SubmitField('Submit')
