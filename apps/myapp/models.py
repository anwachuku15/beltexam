from django.db import models
import re
import datetime
import bcrypt

class UserManager(models.Manager): 
	def reg_validator(self, form):
		errors = {}
		name = form['name']
		username = form['username']
		password = form['password']
		confirm = form['confirm']
		datehired = form['datehired']

		if len(name) < 3:
			errors['name'] = "Name must be 3 characters or more"
		if len(username) < 3:
			errors['username'] = "Username must be 3 characters or more"
		else:
			users = User.objects.filter(username=username)
			if len(users) > 0:
				errors['username'] = 'Username has been taken. Please choose another.'
		if len(password) < 8:
			errors['password'] = "Password must be at least 8 characters"
		elif password != confirm:
			errors['confirm'] = "Passwords do not match"
		if not datehired:
			errors['datehired'] = "Please enter a date"
		elif datehired > str(datetime.datetime.now()):
			errors['datehired'] = "Date hired cannot be a future date."
		return errors

	def loginvalidator(self, form):
		errors = {}
		username = form['username']
		password = form['password']

		if len(username) < 3:
			errors["username"] = "Please enter a valid username"
		elif len(User.objects.filter(username = username)) < 1:
			errors['username'] = "Please register"
		else:
			if not bcrypt.checkpw(password.encode(), User.objects.get(username = username).password.encode()):
				errors['username'] = "Incorrect password. Try again."   
		
		return errors

class ItemManager(models.Manager):
	def item_validator(self, form):
		errors = {}
		name = form['name']

		if len(name) < 4:
			errors["name"] = "Item name should be at least 4 characters"
		return errors  

class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	datehired = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

class Item(models.Model):
	name = models.CharField(max_length=255)
	addedby = models.ForeignKey(User, related_name='itemsuploaded', on_delete=models.CASCADE)
	wishlisted = models.ManyToManyField(User, related_name='wishlisted')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = ItemManager()









