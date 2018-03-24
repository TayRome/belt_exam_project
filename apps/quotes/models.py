from django.db import models
from django.conf import settings
from apps.login.models import Super_User

# Create your models here.
class Quote_Manager(models.Manager):
	def basic_validator(self, postData):
		errors = {}
		if len(postData['author']) < 4:
			errors['author'] = 'Quoted by must be longer than 3 characters'
		if len(postData['quote']) < 11:
			errors['quote'] = 'Quoted by must be longer than 10 characters'
		print(errors)
		return errors

class Quote(models.Model):
	author = models.CharField(max_length=255)
	quote = models.TextField('')
	user = models.ForeignKey(Super_User,on_delete = models.CASCADE, related_name="poster")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = Quote_Manager()

class Favorite(models.Model):
	user = models.ForeignKey(
		Super_User,
		on_delete = models.CASCADE, 
		related_name="favorited_by"
		)

	quote = models.ForeignKey(
		Quote,
		models.SET_NULL, 
		blank=True, 
		null=True, 
		related_name = 'favorite_quotes'
		)
