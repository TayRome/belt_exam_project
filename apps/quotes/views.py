from django.shortcuts import render, redirect
from django.contrib import messages
from apps.login.models import Super_User
from apps.quotes.models import *

# Create your views here.

# quotes 
def all_quotes(request):
	if 'super_user_id' not in request.session:
		return redirect('/')
	super_user = Super_User.objects.get(id=request.session['super_user_id'])
	context = {
		'users': Super_User.objects.all(),
		'super_user': super_user,
		'quotes' : Quote.objects.all(),
		# 'quotes': Quote.objects.exclude(Favorite.objects.filter(user=super_user)),
		'favorites': Favorite.objects.filter(user=super_user)
	}
	return render(request, 'quotes/quotes.html', context)

def post_quote(request):
	if 'super_user_id' not in request.session:
		return redirect('/')
	print('post_quote link good')
	errors = Quote.objects.basic_validator(request.POST)
	if len(errors):
		for tag, error in errors.items():
			messages.error(request, error, extra_tags=tag)
		print('ERRORS!!! OH NOES!!')
		return redirect('/quotes')
	else:
		# User.objects.update_user(request.POST)
		print('no errors')
		Quote.objects.create(
			author = request.POST['author'],
			quote = request.POST['quote'],
			user = Super_User.objects.get(id=request.session['super_user_id'])
			)
		return redirect('/quotes')

def add_favorite(request, id):
	super_user = Super_User.objects.get(id=request.session['super_user_id'])
	Favorite.objects.create(
		user = super_user,
		quote = Quote.objects.get(id=id)
	)
	return redirect('/quotes')

def remove_favorite(request, id):
	Favorite.objects.get(id=id).delete()
	return redirect('/quotes')