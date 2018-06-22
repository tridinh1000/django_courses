from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validatorRegister(self, postData):
        errors = {}
        if not postData['first_name'].isalpha():
            errors["first_name"] = "only letters allowed in first name"
        if not postData['last_name'].isalpha():
            errors["last_name"] = "only letters allowed in last name"
        if len(postData['first_name']) < 3:
            errors["first_name"] = "First name should be at least 3 characters"
        if len(postData['last_name']) < 3:
            errors["last_name"] = "Last name should be at least 3 characters"
        if not EMAIL_REGEX.match(postData['email1']):
            errors["email"] = "Invalid Email Address!"
        if len(postData["email1"]) < 1:
            errors["email"] = "Please enter email address"
        if len(postData['password']) < 8:
            errors["password"] = "Password needs to be more than 8 characters"
        if (postData["password"] != postData["c_password"]):
            errors["passowrd"] = "Passwords do not match"
        if len(User.objects.filter(email=postData["email1"])):
            errors["email"] = "Email already registered"
        return errors

    def basic_validatorLogin(self, postData):
        errors = {}
        # if len(postData["email2"]) < 1:
        #     errors["email"] = "Please enter email address"
        if len(User.objects.filter(email=postData["email2"])) < 1:
            errors["email"] = "Email not registered"
        if not EMAIL_REGEX.match(postData['email2']):
            errors["email"] = "Invalid Email Address!"
        # if len(User.objects.filter(email=postData["email2"])) < 1:
        #     errors["email"] = "Email not registered"
        if len(postData["email2"]) < 1:
            errors["email"] = "Please enter email address"
        if len(postData['password2']) < 8:
            errors["password"] = "Password needs to be more than 8 characters"
        # if len(User.objects.filter(email=postData["email2"])) < 1:
        #     errors["email"] = "Email not registered"
        if len(User.objects.filter(email=postData["email2"])) == 1:
            user = User.objects.get(email=postData['email2'])
            if not bcrypt.checkpw(postData['password2'].encode(), user.password.encode()):
                errors["password"] = "Password doesn't match for provided email"
        return errors

    def basic_validatorAddQuote(self, postData):
        errors = {}
        if len(postData["author"]) < 3:
            errors["author"] = "Author name needs to be more than 3 characters"
        if len(postData["quoteText"]) < 10:
            errors["quoteText"] = "Quote needs to be more than 10 characters"
        return errors

    def basic_validatorUpdateAccount(self, postData, id):
        errors = {}
        user = User.objects.get(id=id)
        if len(postData["first_name"]) < 1:
            errors["first_name"] = "Please enter a first name"
        if len(postData["last_name"]) < 1:
            errors["last_name"] = "Please enter a last name"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid Email Address!"
        if len(postData["email"]) < 1:
            errors["email"] = "Please enter an email name"
        if postData["email"] != user.email:
            if len(User.objects.filter(email=postData["email"])):
                errors["email"] = "Email already registered"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __str__(self):
        return f"User object: {self.first_name} - {self.last_name} - {self.email}"

class Quote(models.Model):
    quote_text = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name="quotes")
    liked_users = models.ManyToManyField(User, related_name="liked_quotes")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __str__(self):
        return f"User object: {self.quote_text} - {self.posted_by}"


