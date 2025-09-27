from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=35)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Такое имя уже существует')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Такая почта уже используется')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Запомни меня')
    submit = SubmitField('Login')

class EditProfileForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(message="Имя пользователя обязательно"),
        Length(min=3, max=50, message="Имя пользователя должно быть от 3 до 50 символов")
    ])

    email = StringField('Email', validators=[
        DataRequired(message="Email обязателен")
    ])

    new_password = PasswordField('Новый пароль')

    confirm_password = PasswordField('Подтвердите новый пароль', validators=[
        EqualTo('new_password', message="Пароли должны совпадать")
    ])

    submit = SubmitField('Сохранить изменения')

    def validate_username(self, username):
        # Проверяем, изменилось ли имя пользователя
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Это имя пользователя уже занято. Выберите другое.')

    def validate_email(self, email):
        # Проверяем, изменился ли email
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Этот email уже зарегистрирован. Используйте другой email.')

    def validate_current_password(self, current_password):
        # Проверяем текущий пароль
        from werkzeug.security import check_password_hash
        if not check_password_hash(current_user.password_hash, current_password.data):
            raise ValidationError('Неверный текущий пароль')