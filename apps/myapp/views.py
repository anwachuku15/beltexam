from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
	return render(request, 'index.html')

def register(request):
	result = User.objects.reg_validator(request.POST)

	if len(result) > 0:
		for key, value in result.items():
			# messages.error(request, value)
			messages.add_message(request, messages.ERROR, value)
		return redirect('/')
	else: # passed validations
		# create the user (add to database)
		hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		user = User.objects.create(name=request.POST['name'], username = request.POST['username'], datehired = request.POST['datehired'], password=hash.decode())
		# print(user.id)
		# save their id in session
		request.session['userid'] = user.id
		# redirect to addmovie page/dashboard
		return redirect('/dashboard')

def login(request):
	result = User.objects.loginvalidator(request.POST)
	if len(result) > 0:
		for key, value in result.items():
			messages.add_message(request, messages.ERROR, value)
		return redirect('/')
	else:
		user = User.objects.get(username = request.POST['username'])
		request.session['userid'] = user.id
		return redirect('/dashboard')

def logout(request):
	request.session.clear()
	return redirect ('/')

def dashboard(request):
	if 'userid' not in request.session:
		return redirect('/')
	else:
		user = User.objects.get(id=request.session['userid'])
		items = user.wishlisted.all()
		otheritems = []
		allitems = Item.objects.all()
		for item in allitems:
			if item not in items:
				otheritems.append(item)

		context = {
			'user': user,
			'items': items,
			'otheritems': otheritems
		}
		return render(request, 'dashboard.html', context)

def wish_items(request, id):
	context = {
		'item': Item.objects.get(id=id),
		'wishlisted': Item.objects.get(id=id).wishlisted.all()
	}
	return render(request, 'wish_items.html', context)

def delete(request, id):
	item = Item.objects.get(id=id)
	item.delete()
	return redirect('/dashboard')

def remove(request, id):
	user = User.objects.get(id=request.session['userid'])
	item = Item.objects.get(id=id)
	user.wishlisted.remove(item)
	return redirect('/dashboard')

def wishlist(request, id):
	user = User.objects.get(id=request.session['userid'])
	item = Item.objects.get(id=id)
	user.wishlisted.add(item)
	return redirect('/dashboard')

def additem(request):
	return render(request, 'create.html')

def processitem(request):
	result = Item.objects.item_validator(request.POST)
	if len(result) > 0:
		for key, value in result.items():
			messages.add_message(request, messages.ERROR, value)
		return redirect('/create')
	else:
		item = Item.objects.create(name=request.POST['name'], addedby_id=request.session['userid'])
		user = User.objects.get(id = request.session['userid'])
		user.wishlisted.add(item)
		return redirect('/dashboard')

















































