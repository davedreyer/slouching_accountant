from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from django.shortcuts import render, redirect
import bcrypt
import re

class UserManager(models.Manager):
	def reg_check(self, postData):

		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		# checks for a valid email format: email@email.com

		name_match = r'^[a-zA-Z]+$'	
		# accepts only alpha characters in a name

		pass_require = r'(?=.*[A-Z]+)(?=.*[0-9]+)'
		# password requires at least one upper case letter and one number

		birthdate_match = r'^(0[1-9]|1[0-2])\/(0[1-9]|1\d|2\d|3[01])\/(19|20)\d{2}$'

		error_messages = []

		if len(postData['name']) < 2:
			error_messages.append('Name must contain at least 2 characters!')
			
		if not re.search(name_match, postData['name']):
			error_messages.append('Name must have only letters!')
			
		if len(postData['alias']) < 2:
			error_messages.append('Alias must contain at least 2 characters!')
			
		if not re.search(name_match, postData['alias']):
			error_messages.append('Alias must have only letters!')
				
		if not postData['email']:
			error_messages.append('Email address is required!')
			
		if not EMAIL_REGEX.match(postData['email']):
			error_messages.append('Email address needs to be in a valid format!')

		else:
			email_check = self.filter(email=postData['email'])
			if email_check:
				error_messages.append('Email address is already in the database!')	
			
		if not postData['password']:
			error_messages.append("Password cannot be blank! Password must be at least 8 characters and contain at least 1 capital letter and 1 number!")
		
		else:	
			if len(postData['password']) < 8:
				error_messages.append("Password cannot be less than 8 characters!")
				
			if not re.search(pass_require, postData['password']):
				error_messages.append("Password must contain at least 1 capital letter and 1 number!")
				
		if postData['confirm_password'] != postData['password']:
			error_messages.append("Confirm password and password must match!")

		if not postData['birthdate']:
			error_messages.append("Birthdate must be entered and format should be MM/DD/YYYY")

		if not re.search(birthdate_match, postData['birthdate']):
			error_messages.append("Birthdate must be entered in format of MM/DD/YYYY")
					
		response = {}				

		if error_messages:
			response['errors'] = error_messages
			response['created'] = False

		else:
			pw_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
			new_user = self.create(email=postData['email'],name=postData['name'],alias=postData['alias'],birthdate=postData['birthdate'],pw_hash=pw_hash)
			response['created'] = True
			response['new_user'] = new_user

		return response

	def login_check(self, postData):

		error_messages = []
		email_check = User.objects.filter(email=postData['email'])
		response = {}

		if not email_check:
			error_messages.append("Email does not exist in system! Please register!")
			response['login'] = False
		else:
			if bcrypt.hashpw(postData['password'].encode(), email_check[0].pw_hash.encode()) == email_check[0].pw_hash:
				response['login'] = True
				response['user'] = email_check[0]
			else:	
				error_messages.append("Password is invalid!")
				response['login'] = False

		response['errors'] = error_messages

		return response	
						
class User(models.Model):
	name=models.CharField(max_length=100)
	alias=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	birthdate = models.CharField(max_length=10)
	pw_hash=models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	objects = UserManager()
