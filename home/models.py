from enum import unique
from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        # Length of first name 
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name requires at least 2 characters; letters only.'
        # Length of last name
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last Name requires at least 2 characters; letters only.'
        # Email matches format 
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email']) == 0:
            errors['email'] = 'You must enter an email.'
        elif not email_regex.match(postData['email']):
            errors['email'] = 'Must be a valid email.'
        # Email is unique 
        current_users = User.objects.filter(email = postData['email'])
        if len(current_users) > 0:
            errors['duplicate'] = 'Email is already in use.'
        # Password was entered (more than 8) 
        if len(postData['password']) < 8:
            errors['password'] = 'Password requires at least 8 characters.'
        if postData['password'] != postData['confirm_password']:
            errors['mismatch'] = 'Password confirmation must match original password.'
        return errors

    def log_validator(self, postData):
        errors = {}
        existing_user = User.objects.filter(email = postData['email'])
        # Email has been entered 
        if len(postData['email']) == 0:
            errors['email'] = 'Email must be entered.'
        # Password has been entered 
        if len(postData['password']) < 8:
            errors['password'] = 'Password requires at least 8 characters.'
        # Email and Password match an registered account 
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
            errors['password'] = 'Email and password do not match.'
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=55)
    last_name=models.CharField(max_length=55)
    email=models.CharField(max_length=55)
    password=models.CharField(max_length=55)
    objects = UserManager()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
