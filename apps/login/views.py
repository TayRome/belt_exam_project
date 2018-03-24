from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from apps.login.models import Super_User
from .models import Super_User

# Create your views here.
# landing page
def index(request):
	if 'super_user_id' not in request.session:
		request.session['status'] = 'guest'
		return render(request, 'login/login.html')
	else:
		request.session['status'] = 'logged_in'
		return render(request, 'login/login.html', {'super_user': Super_User.objects.get(id=request.session['super_user_id'])})

# register new super_user
def register(request):
	result = Super_User.objects.validate_registration(request.POST)
	if result['status'] != True:
		for error in result['errors']:
			messages.error(request, result['errors'][error])
		return redirect('/')
	else:
		request.session['super_user_id'] = result['super_user_id']
		return redirect('quotes/')

# log in existing super_user
def login(request):
	result = Super_User.objects.validate_login(request.POST)
	if result['status'] != True:
		for error in result['errors']:
			messages.error(request, result['errors'][error])
		return redirect('/')
	else:
		request.session['super_user_id'] = result['super_user_id']
		return redirect('quotes/')

# clear request.session data
def logout(request):
	request.session.flush()
	return redirect('/')
