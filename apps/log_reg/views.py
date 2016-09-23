from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User

def index(request):
	if request.method=="GET":
		return render(request, 'log_reg/index.html')

	if request.method=="POST":
		if request.POST['process'] == 'registration':
			check = User.objects.reg_check(request.POST)
			if check['created']:
				request.session['user'] = {
			        'id' : check['new_user'].id,
			        'name' : check['new_user'].name,
			        'alias' : check['new_user'].alias,
			        'email' : check['new_user'].email,
			    }
				messages.success(request, "Success! Welcome {}!".format(request.session['user']['name']))
				return redirect(reverse('cool_app:index'))	

			else:
				for x in check['errors']:
					messages.error(request, x)
				return redirect(reverse('authenticate:index'))

		elif request.POST['process'] == 'login':
			check = User.objects.login_check(request.POST)
			if check['login'] == True:
				request.session['user'] = {
			        'id' : check['user'].id,
			        'name' : check['user'].name,
			        'alias' : check['user'].alias,
			        'email' : check['user'].email,
			    }
				messages.success(request, "Hi {}! You successfully logged in!".format(request.session['user']['name']))
				return redirect(reverse('cool_app:index'))
			else:
				for x in check['errors']:
					messages.error(request, x)
				return redirect(reverse('authenticate:index'))		

def logout(request):
	if request.method=="GET":
		del request.session['user']
		messages.success(request, 'Success! You were logged out!')
		return redirect(reverse('authenticate:index'))				

def success(request):
	if request.method=="GET":
		if not 'user' in request.session:
			messages.error(request, "Sorry you are not logged in!")
			return redirect(reverse('authenticate:index'))
		else:	
			return render(request, 'log_reg/success.html')		
