from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from banque.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')
    first_name=StringField(label='First name',validators=[DataRequired()])
    last_name=StringField(label='Last name',validators=[DataRequired()])
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    numero = StringField(label='Telephone:', validators=[DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    question1=StringField(label='Question1:', validators=[DataRequired()])
    reponse1=StringField(label='Reponse1:', validators=[DataRequired()])
    submit = SubmitField(label='Create Account')

class QuestionForm(FlaskForm):
    question1=StringField(label='Question1:', validators=[DataRequired()])
    reponse1=StringField(label='Reponse1:', validators=[DataRequired()])
    # à modifier(utilisation de select ) ...
    # question2=StringField(label='Question2:', validators=[DataRequired()])
    # reponse2=StringField(label='Reponse2:', validators=[DataRequired()])
    # question3=StringField(label='Question3:', validators=[DataRequired()])
    # reponse3=StringField(label='Reponse3:', validators=[DataRequired()])
    # submit = SubmitField(label='Envoie code')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    code = StringField(label='Code bancaire:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class TransactionForm(FlaskForm):

    code = StringField(label='Code bancaire:', validators=[DataRequired()])
    receiver = StringField(label='receiver Name:', validators=[DataRequired()])
    montant = IntegerField(label='montant:', validators=[DataRequired()])
    submit = SubmitField(label='Send')

class VerifyForm(FlaskForm):
    question=StringField(label='Repondre à la question suivante')
    reponse=StringField(label='Votre réponse')
    submit = SubmitField(label='submit')
