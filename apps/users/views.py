from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from apps.login.models import Super_User
from apps.quotes.models import Quote

# Create your views here.

def index(request):
	return HttpResponse('worked')

def view_user(request, id):
	print('link ist bueno')
	if 'super_user_id' not in request.session:
		return redirect('/')
	context = {
		'user': Super_User.objects.get(id=id),
		'quotes': Quote.objects.filter(user=id),
		'count': Quote.objects.filter(user=id).count(),
	}


	return render(request, 'users/users.html', context)