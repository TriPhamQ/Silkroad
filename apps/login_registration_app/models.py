from django.db import models
import re, bcrypt

# REGEX     =   =   =   =   =   =   =   =   =   =   =   =   =   =   =   =   =   =   =   =   =
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{8,30}$')

# Manager for models    =   =   =   =   =   =   =   =   =   =   =   =   =   =   =   =   =   =
class UserManager(models.Manager):
    def validate_registration(self, form):
        self.form = form
        self.errors = []

        # First Name
        if len(self.form['first_name']) == 0:
            self.errors.append("First name is required")
        elif not self.form['first_name'].isalpha():
            self.errors.append("First name must only consist of letters")

        # Last Name
        if len(self.form['last_name']) == 0:
            self.errors.append("Last name is required")
        elif not self.form['last_name'].isalpha():
            self.errors.append("Last name must only consist of letters")

        # Email
        if len(self.form['email']) == 0:
            self.errors.append("Email is required")
        elif not EMAIL_REGEX.match(self.form['email']):
            self.errors.append("Please enter a valid email address")
        elif User.objects.filter(email = self.form['email']):
            self.errors.append("Account already exist for this email")

        # Password
        if len(self.form['password']) == 0:
            self.errors.append("Password is required")
        elif len(self.form['password']) < 9:
            self.errors.append("Password must be longer than 8 characters length")
        elif not PASSWORD_REGEX.match(self.form['password']):
            self.errors.append("Password must have atleast one number, one upper case, one lower case characters")

        # Password confirmation
        if self.form['password'] != self.form['password_confirmation']:
            self.errors.append("Password confirmation does not match")

        return self.errors

    def register(self, form):
        hashed_pass = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())

        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            password = hashed_pass
        )

    def login(self, form):
        check_user = self.filter(email = form['email'].lower())
        if check_user and bcrypt.checkpw(form['password'].encode(), check_user[0].password.encode()):
            return check_user[0]
        else:
            return None



# Create your models here   =    =   =   =   =   =   =   =   =   =   =   =   =   =   =   =   =
class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=30)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
