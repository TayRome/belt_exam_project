from django.db import models
from django.conf import settings
import re, bcrypt
# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Super_User_Manager(models.Manager):

	##### REGISTRATION VALIDATION #####
	def validate_registration(self, postData):
		print('validation started')
		result = {
			'status' : False,
			'errors' : {}
		}

		# name field validation
		if postData['name'] == '':
			result['errors']['name'] = 'Name cannot be blank'
		if postData['alias'] == '':
			result['errors']['alias'] = 'Last name cannot be blank'

		# email field validation
		if postData['email'] == '':
			result['errors']['email'] = 'Email cannot be blank'
		if not EMAIL_REGEX.match(postData['email']):
			result['errors']['email'] = 'Invalid Email Address'
		existing = Super_User.objects.filter(email = postData['email'])
		if existing:
			result['errors']['email'] = 'Email already registered, please log in instead.'

		# password field validation
		if postData['password'] != postData['cpassword']:
			result['errors']['password'] = 'Passwords do not match'
		if len(postData['password']) <8:
			result['errors']['password'] = 'Passwords must be at least 8 characters long.' 

		if len(result['errors']):
			return result
		else:
		# create new super_user
			user_password = postData['password'] 
			hashed = bcrypt.hashpw(user_password.encode(), bcrypt.gensalt())
			new_super_user = Super_User.objects.create(
				name = postData['name'],
				alias = postData['alias'],
				email = postData['email'],
				password = hashed,
				birthday = postData['birthday'],
				)
			result['status'] = True
			result['super_user_id'] = new_super_user.id
			return result

	##### LOGIN VALIDATION #####
	def validate_login(self, postData):
		result = {
			'status' : False,
			'errors' : {}
		}

		# email validation
		existing = Super_User.objects.filter(email = postData['email'])
		if existing:
			# password validation
			# .encode().decode().encode()
			user_password = postData['password'].encode()
			# this is magic....
			existing_password = existing[0].password[2: len(existing[0].password) - 1]
			existing_password = existing_password.encode()
			if not bcrypt.checkpw(user_password, existing_password):
				result['errors']['password'] = 'Password doesn\'t match'
		else:
			result['errors']['password'] = 'Email not found'

		if len(result['errors']):
			return result
		else:
			result['status'] = True
			result['super_user_id'] = existing[0].id
			return result

# define super_user
class Super_User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	birthday = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = Super_User_Manager()
