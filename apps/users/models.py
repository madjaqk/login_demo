import re

from django.db import models
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
	def register(self, data):
		errors = []

		if not data["email"]:
			errors.append("E-mail can't be blank")
		elif not EMAIL_REGEX.match(data["email"]):
			errors.append("Invalid E-mail")
		elif self.filter(email=data["email"]):
			errors.append("E-mail in use")

		if not data["password"]:
			errors.append("Password can't be blank")
		elif len(data["password"]) < 8:
			errors.append("Password must be at least 8 characters long")
		elif data["password"] != data["confirm"]:
			errors.append("Password and confirmation don't match")

		response = {}

		if errors:
			response["registered"] = False
			response["errors"] = errors
		else:
			password = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())
			user = self.create(email=data["email"], password=password)

			response["registered"] = True
			response["user"] = user

		return response

	def login(self, data):
		user = self.filter(email=data["email"])

		if not user:
			return False
		else:
			user = user[0]

		if bcrypt.hashpw(data["password"].encode(), user.password.encode()) == user.password.encode():
			return user
		else:
			return False

class User(models.Model):
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()