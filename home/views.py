from django.shortcuts import render, redirect
from django.contrib import messages
from . models import User, UserManager
import bcrypt

# Create your views here. 

# Render the index page 
def index(request):
    request.session.flush()
    return render(request, 'index.html')

# Validate the registration
def register(request):
    if request.method == 'POST':
        errors = User.objects.reg_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        # Hash the password
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        # Create the user
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_pw,
        )
        # Create a session  
        request.session['user_id']= new_user.id
        return redirect('/success')
    return redirect('/')

# Render the success page
def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    context = {
        'user': this_user[0]
    }
    return render(request, 'success.html', context)

# Log in 
def login(request):
    if request.method == 'POST':
        errors = User.objects.log_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.filter(email = request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect('/success')
    return redirect('/')

# Log out 
def logout(request):
    request.session.flush()
    return redirect('/')
